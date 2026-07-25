# Model Admission Status

OpenDub separates research provenance from product availability. A repository appearing in this
table is not evidence that its model is installed, usable, or licensed for a particular workflow.

| Upstream | Current status | What is verified | What remains before product use |
| --- | --- | --- | --- |
| EmoDubber | Planned | Fixed source commit and source-code audit record | Weight terms/checksum, reproducible inference, adapter contract, real smoke, and control-effect evidence |
| HPMDubbing | Planned | Fixed source commit and source-code audit record | Video preprocessing contract, weight terms/checksum, reproducible inference, adapter contract, and real smoke |
| HPMDubbing_Vocoder | Planned | Fixed source commit, source license, audio configuration notes | Weight terms/checksum, isolated adapter, output smoke, and compatibility tests |
| StyleDubber | Planned | Fixed source commit in registry | Source/weight/license audit and adapter validation |
| HDCode | Planned | Fixed source commit, MIT source license, 22.05 kHz README contract | Checkpoint/feature availability, weight terms/checksum, isolated runtime, and real smoke |
| CoSyncDiT, LLM-Flow-Dubber | Planned | Research references only where recorded | Public code/weights/license and the full admission process |

The machine-readable source of truth is [`model-registry/upstreams.yaml`](../../model-registry/upstreams.yaml).
Audits live under [`docs/audits/`](../audits/). An adapter can move to `experimental` only when
the repository, source commit, source license, weights, input contract, and at least one real
inference have been verified. It can move to `stable` only after a controlled real smoke test,
documented limits, and release-quality reproducibility evidence.
