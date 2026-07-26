import json
from pathlib import Path

import pytest

from opendub.application.preparation_service import PreparationService, target_text_fingerprint
from opendub.domain.assets import ConsentRecord, InputAuthorization, MediaAsset, VoiceReference
from opendub.domain.errors import DomainError
from opendub.domain.project import MethodSelection, Project
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.storage.project_store import ProjectStore


def test_preparation_export_is_bound_to_selected_method_authorized_inputs_and_timeline(
    tmp_path: Path,
) -> None:
    project = _prepared_project()
    store = ProjectStore(tmp_path)
    store._write_project(project)

    result = PreparationService(store).export(project.id)
    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "opendub.project-preparation/v1"
    assert manifest["project"]["id"] == project.id
    assert manifest["method_selection"]["method_id"] == "galaxycong/emodubber"
    assert manifest["inputs"]["video"]["sha256"] == "a" * 64
    assert manifest["inputs"]["target_text"]["sha256"] == target_text_fingerprint(project.segments)
    assert manifest["inputs"]["reference_speech"][0]["consent_id"] == project.consents[0].id
    assert manifest["segments"][0]["range"] == {"start_us": 0, "end_us": 1_200_000}


def test_preparation_export_refuses_an_unapproved_target_text_state(tmp_path: Path) -> None:
    project = _prepared_project()
    project = project.model_copy(
        update={
            "input_authorizations": tuple(
                item for item in project.input_authorizations if item.input_kind == "video"
            )
        }
    )
    store = ProjectStore(tmp_path)
    store._write_project(project)

    with pytest.raises(DomainError, match="target text authorization") as error:
        PreparationService(store).export(project.id)

    assert error.value.code == "RIGHTS_DECLARATION_REQUIRED"


def _prepared_project() -> Project:
    video = MediaAsset(
        kind="video",
        display_name="authorized-scene.mp4",
        relative_path="assets/authorized-scene.mp4",
        sha256="a" * 64,
        size_bytes=1024,
        duration_us=2_000_000,
    )
    voice_audio = MediaAsset(
        kind="audio",
        display_name="authorized-reference.wav",
        relative_path="assets/authorized-reference.wav",
        sha256="b" * 64,
        size_bytes=512,
        duration_us=1_500_000,
    )
    consent = ConsentRecord(material_source="self_recorded")
    reference = VoiceReference(
        asset_id=voice_audio.id,
        consent_id=consent.id,
        speaker_label="Authorized actor",
    )
    segment = DubbingSegment(
        range=TimeRange(start_us=0, end_us=1_200_000),
        text="A locally authorized target line.",
        language="en",
        character_id=reference.id,
        voice_reference_id=reference.id,
        emotion=EmotionSpec(label="happy", intensity=0.7),
        adapter_id="galaxycong/emodubber",
        status="ready",
    )
    return Project(
        name="Prepared authorized scene",
        assets=(video, voice_audio),
        consents=(consent,),
        voice_references=(reference,),
        input_authorizations=(
            InputAuthorization(
                input_kind="video",
                asset_id=video.id,
                content_sha256=video.sha256,
                material_source="self_recorded",
            ),
            InputAuthorization(
                input_kind="target_text",
                content_sha256=target_text_fingerprint((segment,)),
                material_source="self_recorded",
            ),
        ),
        method_selection=MethodSelection(
            method_id="galaxycong/emodubber",
            method_manifest_version="method-manifest@553fa054",
            declared_need="Use explicit emotion control.",
            required_inputs=("Video", "Target text", "Authorized reference speech"),
            optional_controls=("Emotion category", "Emotion intensity"),
            runtime_status="unavailable",
            content_modes=("concept",),
            evidence_revision="553fa054",
        ),
        segments=(segment,),
    )
