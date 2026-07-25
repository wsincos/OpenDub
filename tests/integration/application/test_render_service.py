import json
from pathlib import Path

import soundfile as sf

from opendub.application.generation_service import GenerationService
from opendub.application.render_service import RenderService
from opendub.domain.assets import ConsentRecord, VoiceReference
from opendub.domain.ids import new_id
from opendub.domain.segments import DubbingSegment, EmotionSpec
from opendub.domain.time import TimeRange
from opendub.models.testing import DeterministicTestAdapter
from opendub.storage.artifact_store import ArtifactStore
from opendub.storage.project_store import ProjectStore


def test_render_service_assembles_an_accepted_candidate_to_wav(tmp_path: Path) -> None:
    store = ProjectStore(tmp_path)
    project = store.create("Renderable project")
    reference_asset = ArtifactStore(tmp_path).ingest_bytes(
        project.id,
        kind="audio",
        display_name="authorized-reference.wav",
        data=b"test-only reference",
        extension="wav",
    )
    project = project.add_asset(reference_asset, expected_revision=project.revision)
    store.save(project, expected_revision=1)
    consent = ConsentRecord(material_source="self_recorded")
    reference = VoiceReference(
        asset_id=reference_asset.id,
        consent_id=consent.id,
        speaker_label="Test narrator",
    )
    project = project.add_voice_reference(consent, reference, expected_revision=project.revision)
    store.save(project, expected_revision=2)
    segment = DubbingSegment(
        range=TimeRange(start_us=0, end_us=1_000_000),
        text="Render this accepted candidate.",
        language="en",
        character_id=new_id(),
        voice_reference_id=reference.id,
        emotion=EmotionSpec(label="neutral", intensity=0.5),
        adapter_id="opendub.test",
        status="ready",
    )
    project = project.add_segment(segment, expected_revision=project.revision)
    store.save(project, expected_revision=3)
    candidate = GenerationService(store, DeterministicTestAdapter()).generate_segment(
        project.id, segment.id, expected_revision=project.revision, seed=3
    )
    generated = store.load(project.id)
    accepted = generated.accept_candidate(
        segment.id, candidate.id, expected_revision=generated.revision
    )
    store.save(accepted, expected_revision=generated.revision)

    result = RenderService(store).render(project.id, mode="remove")
    audio, sample_rate = sf.read(result.dubbing_audio, dtype="float32")

    assert result.dubbing_audio.is_file()
    assert result.manifest.is_file()
    assert result.video is None
    assert sample_rate == 24_000
    assert len(audio) == 24_000
    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))
    assert manifest["content_label"] == "AI-generated dubbing by OpenDub"
    assert manifest["mix_mode"] == "remove"
    assert manifest["project_revision"] == accepted.revision
