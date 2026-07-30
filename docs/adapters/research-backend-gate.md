# Research Backend Promotion Gate

An upstream paper, repository, demo page, or checkpoint link is research provenance. It is not a
runnable OpenDub capability. This gate applies equally to external, team-authored, and future
research backends.

## Registry States

| State | User-visible meaning | Minimum evidence |
| --- | --- | --- |
| `planned` | Research direction only; Studio must not offer generation | Review note explaining the missing evidence |
| `experimental` | A controlled adapter can be used with stated limits | Fixed source commit and source license, immutable weight SHA-256 and terms, adapter version, input contract, real smoke report |
| `stable` | A release-supported adapter | Experimental evidence plus controlled reproducibility, control-effect testing, known limits, and release validation |

The registry validator requires `admission.adapter_version`, `admission.input_contract`, and
`admission.real_smoke_report` for `experimental` and `stable` records. Planned records deliberately
do not receive an admission block.

## Required Promotion Packet

1. A pinned 40-character source commit, source license record, and a summary of copied or patched
   upstream files.
2. Every required model artifact with a stable URL or distribution record, explicit usage terms,
   byte size, and SHA-256.
3. A versioned input/output contract that records video frame rate, audio sample rate, feature
   shapes, language limits, and preprocessing requirements.
4. An isolated adapter environment report that does not modify global packages or require manual
   `site-packages` edits.
5. A real inference smoke report using authorized fixtures, including command, hardware, elapsed
   time, peak memory when available, output hashes, and failure limitations.
6. A control-effect result for every control exposed in Studio. A parameter that cannot show a
   measurable or inspectable effect must remain unavailable in the UI.

## Current Dispositions

The exact public upstream status remains in
[`config/model-registry/upstreams.yaml`](../../config/model-registry/upstreams.yaml). As of the recorded audits,
EmoDubber, HPMDubbing, StyleDubber, HPMDubbing Vocoder, HDCode, CoSyncDiT, and LLM-Flow-Dubber
remain `planned`. None may be presented as an installed OpenDub model.
