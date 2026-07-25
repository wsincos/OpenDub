"""Pydantic contracts for evidence-bound Method Atlas content."""

from __future__ import annotations

from datetime import datetime
from pathlib import PurePosixPath
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator
from pydantic_core import PydanticCustomError

MethodId = Literal[
    "galaxycong/hpmdubbing",
    "galaxycong/styledubber",
    "galaxycong/emodubber",
]


class AtlasValidationError(ValueError):
    """A concise error used by content tooling and tests."""


class AtlasModel(BaseModel):
    """Strict base model that retains structured Pydantic validation internally."""

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        extra: Literal["allow", "ignore", "forbid"] | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        try:
            return super().model_validate(
                obj,
                strict=strict,
                extra=extra,
                from_attributes=from_attributes,
                context=context,
                by_alias=by_alias,
                by_name=by_name,
            )
        except ValidationError as error:
            first = error.errors(include_url=False)[0]
            code = str(first.get("type", "ATLAS_VALIDATION_ERROR")).upper()
            raise AtlasValidationError(code) from error


class LocalizedText(AtlasModel):
    zh_cn: str = Field(min_length=1, max_length=1000)
    en: str = Field(min_length=1, max_length=1000)


class PaperReference(AtlasModel):
    title: str = Field(min_length=1, max_length=500)
    url: str = Field(pattern=r"^https://")


class SourceReference(AtlasModel):
    repository: str = Field(pattern=r"^https://github\.com/")
    commit: str = Field(pattern=r"^[0-9a-f]{40}$")


class PaperAnchor(AtlasModel):
    section: str = Field(min_length=1, max_length=100)
    url: str = Field(pattern=r"^https://")


class CodeAnchor(AtlasModel):
    path: str = Field(min_length=1, max_length=500)
    url: str = Field(pattern=r"^https://")


class CitationReference(AtlasModel):
    key: str = Field(min_length=1, max_length=200)
    label: str = Field(min_length=1, max_length=300)
    url: str = Field(pattern=r"^https://")


class ControlDescriptor(AtlasModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    label: LocalizedText
    kind: Literal["select", "range", "toggle"]
    explanation: LocalizedText


class SignalDescriptor(AtlasModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_.-]*$")
    type: Literal[
        "video.scene",
        "video.face_roi",
        "video.lip_roi",
        "text.transcript",
        "text.phonemes",
        "audio.reference",
        "audio.generated",
        "acoustic.mel",
        "prosody.duration",
        "prosody.f0",
        "prosody.energy",
        "emotion.valence_arousal",
        "emotion.category",
        "alignment.matrix",
        "embedding.projection",
        "flow.trajectory",
        "metric.scalar",
    ]
    label: LocalizedText
    unit: str | None = Field(default=None, max_length=100)
    time_binding: Literal["none", "intervals", "uniform", "media_pts"]
    renderer: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    explanation: LocalizedText


class MethodNode(AtlasModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    label: LocalizedText
    short_label: str = Field(min_length=1, max_length=40)
    kind: Literal[
        "input",
        "visual",
        "text",
        "voice",
        "alignment",
        "prosody",
        "style",
        "emotion",
        "acoustic",
        "generation",
        "output",
    ]
    summary: LocalizedText
    solves: LocalizedText
    consumes: list[str]
    produces: list[str]
    paper_refs: list[PaperAnchor] = Field(min_length=1)
    code_refs: list[CodeAnchor]
    visualization_slots: list[str]
    group: str | None = None


class MethodEdge(AtlasModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    source: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    target: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    signal_ids: list[str]
    label: LocalizedText | None = None


class MethodGroup(AtlasModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    label: LocalizedText
    node_ids: list[str]


class MethodGraph(AtlasModel):
    nodes: list[MethodNode] = Field(min_length=2)
    edges: list[MethodEdge]
    groups: list[MethodGroup]
    overview_path: list[str] = Field(min_length=2)
    layout: Literal["left-to-right"]


class MethodChapter(AtlasModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    label: LocalizedText
    node_ids: list[str]


class MethodManifest(AtlasModel):
    schema_version: Literal["opendub.method/v1"]
    id: MethodId
    slug: Literal["hpmdubbing", "styledubber", "emodubber"]
    title: str = Field(min_length=1, max_length=500)
    short_title: str = Field(min_length=1, max_length=100)
    conference: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=2020, le=2100)
    question: LocalizedText
    contribution: LocalizedText
    paper: PaperReference
    source: SourceReference
    runtime_status: Literal["unavailable", "experimental", "stable"]
    content_modes: list[Literal["concept", "replay", "live", "planned"]] = Field(min_length=1)
    required_inputs: list[Literal["video", "text", "reference_speech"]] = Field(min_length=3)
    optional_controls: list[ControlDescriptor]
    signals: list[SignalDescriptor] = Field(min_length=1)
    graph: MethodGraph
    chapters: list[MethodChapter]
    citations: list[CitationReference]

    @model_validator(mode="after")
    def verify_semantics(self) -> Self:
        node_ids = {node.id for node in self.graph.nodes}
        if len(node_ids) != len(self.graph.nodes):
            raise PydanticCustomError("ATLAS_NODE_ID_DUPLICATE", "Method node IDs must be unique")
        signal_ids = {signal.id for signal in self.signals}
        for edge in self.graph.edges:
            if edge.source not in node_ids:
                raise PydanticCustomError(
                    "ATLAS_EDGE_SOURCE_MISSING", "Method edge source is not a declared node"
                )
            if edge.target not in node_ids:
                raise PydanticCustomError(
                    "ATLAS_EDGE_TARGET_MISSING", "Method edge target is not a declared node"
                )
            if edge.source == edge.target:
                raise PydanticCustomError(
                    "ATLAS_EDGE_SELF_LOOP", "Method graph cannot contain self loops"
                )
            unknown_signals = set(edge.signal_ids) - signal_ids
            if unknown_signals:
                raise PydanticCustomError(
                    "ATLAS_EDGE_SIGNAL_MISSING", "Method edge references an unknown signal"
                )
        for node in self.graph.nodes:
            if not set(node.visualization_slots) <= signal_ids:
                raise PydanticCustomError(
                    "ATLAS_NODE_SIGNAL_MISSING", "Method node references an unknown signal"
                )
        if not set(self.graph.overview_path) <= node_ids:
            raise PydanticCustomError(
                "ATLAS_OVERVIEW_NODE_MISSING", "Overview path references an unknown node"
            )
        if self.graph.nodes[0].kind == "output":
            raise PydanticCustomError("ATLAS_GRAPH_INPUT_MISSING", "Graph must start with an input")
        if not any(node.kind == "output" for node in self.graph.nodes):
            raise PydanticCustomError("ATLAS_GRAPH_OUTPUT_MISSING", "Graph must include an output")
        return self


class AssetReference(AtlasModel):
    path: str = Field(min_length=1, max_length=500)
    media_type: str = Field(min_length=1, max_length=120)
    byte_size: int = Field(gt=0)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    duration_us: int | None = Field(default=None, gt=0)
    width: int | None = Field(default=None, gt=0)
    height: int | None = Field(default=None, gt=0)
    sample_rate: int | None = Field(default=None, gt=0)
    channels: int | None = Field(default=None, gt=0)

    @field_validator("path")
    @classmethod
    def verify_relative_path(cls, value: str) -> str:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or ":" in value:
            raise PydanticCustomError("ATLAS_ASSET_PATH_INVALID", "Asset path must be relative")
        return value


class RightsRecord(AtlasModel):
    video_source: Literal["self_created", "public_domain", "licensed", "authorized_other"]
    voice_source: Literal["self_recorded", "public_domain", "licensed", "authorized_other"]
    text_source: Literal["self_created", "public_domain", "licensed", "authorized_other"]
    public_display_allowed: bool
    redistribution_allowed: bool
    evidence_path: str = Field(min_length=1, max_length=500)
    reviewer: str = Field(min_length=1, max_length=200)
    reviewed_at: datetime


class TimeBase(AtlasModel):
    kind: Literal["none", "intervals", "uniform", "media_pts"]
    start_us: int | None = None
    hop_us: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def verify_uniform(self) -> Self:
        if self.kind == "uniform" and (self.start_us is None or self.hop_us is None):
            raise PydanticCustomError(
                "ATLAS_TIME_BASE_INCOMPLETE", "Uniform signal time base needs start_us and hop_us"
            )
        return self


class SignalArtifact(AtlasModel):
    signal_id: str = Field(pattern=r"^[a-z][a-z0-9_.-]*$")
    mode: Literal["concept", "replay", "live"]
    illustrative: bool
    asset: AssetReference
    time_base: TimeBase | None = None
    shape: list[int] | None = None
    dtype: str | None = None
    normalization: str | None = None

    @model_validator(mode="after")
    def verify_mode(self) -> Self:
        if self.mode in {"replay", "live"} and self.illustrative:
            raise PydanticCustomError(
                "ATLAS_REPLAY_ILLUSTRATIVE", "Replay and live signals cannot be illustrative"
            )
        return self


class ReplayProvenance(AtlasModel):
    mode: Literal["historical_demo", "opendub_run", "author_export"]
    source_commit: str | None = Field(default=None, pattern=r"^[0-9a-f]{40}$")
    adapter_version: str | None = None
    weights_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    run_manifest_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    parameters: dict[str, Any]
    limitations: list[str]


class MetricResult(AtlasModel):
    metric_id: str = Field(pattern=r"^[a-z][a-z0-9_.-]*$")
    version: str = Field(min_length=1, max_length=100)
    status: Literal["ok", "not_applicable", "unavailable", "failed"]
    value: float | None = None
    unit: str | None = None
    higher_is_better: bool | None = None
    preprocessing_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class ReplayBundle(AtlasModel):
    schema_version: Literal["opendub.replay/v1"]
    id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    case_id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    method_id: MethodId
    created_at: datetime
    provenance: ReplayProvenance
    rights: RightsRecord
    output_speech: AssetReference
    dubbed_video: AssetReference | None = None
    signals: list[SignalArtifact]
    metrics: list[MetricResult]

    @model_validator(mode="after")
    def verify_replay(self) -> Self:
        if not self.rights.public_display_allowed:
            raise PydanticCustomError(
                "ATLAS_REPLAY_PUBLIC_DISPLAY_FORBIDDEN", "Replay cannot be published"
            )
        if not self.signals:
            raise PydanticCustomError(
                "ATLAS_REPLAY_SIGNALS_MISSING", "Replay needs at least one signal"
            )
        return self
