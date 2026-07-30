# Real Backend Admission Handoff

This checklist is for the project owner or upstream maintainer who can authorize an OpenDub
adapter. It is deliberately artifact-specific: source-code access or a public Drive link alone
does not make a backend runnable or distributable.

## Submit One Backend First

Choose exactly one starting backend, preferably the most complete reproducible inference path.
Do not combine EmoDubber, HPMDubbing, StyleDubber, and a vocoder in one admission request. Each
model and each weight artifact has its own license, input contract, and smoke-test evidence.

The first candidate should provide waveform output from a short authorized fixture without
requiring unpublished dataset files or modifications to Python site-packages.

## Required Artifact Packet

For every checkpoint, encoder, vocoder, tokenizer, or auxiliary model used by the chosen path,
provide all of the following in writing:

| Required item | Acceptable evidence |
| --- | --- |
| Exact upstream source | Repository URL and immutable 40-character commit |
| Artifact identity | Filename, byte size, SHA-256, and immutable download location or owner-supplied local path |
| Distribution terms | License text or written authorization covering evaluation, local inference, and the intended OpenDub release scope |
| Runtime recipe | Python, CUDA, PyTorch, package versions, command, expected GPU memory, and required environment variables |
| Input contract | Required video/audio/text/features, sample rate, frame rate, feature cadence, mel hop/window/bin count, and reference-audio requirements |
| Authorized smoke fixture | A short input package with an asset-rights declaration and expected output properties |
| Attribution | Paper citation, upstream repository citation, and any required notices |

Do not send private credentials, signing keys, personal voice recordings, restricted movie clips,
or copyrighted V2C data. Store legal authorization records in the team-controlled archive, not in
the public repository.

## Acceptance Sequence

1. Add the source and artifact packet to the private review record.
2. Verify the artifact size and SHA-256 before opening it in an isolated runtime.
3. Add a `planned` registry admission record with the review evidence.
4. Build the adapter in a separate worker environment. The core OpenDub process must not import
   the research runtime.
5. Run one authorized fixture end to end and save a redacted run manifest with input/output
   hashes, runtime versions, timing, and peak memory.
6. Validate that every declared capability is actually accepted by the adapter. In particular,
   do not declare emotional strength, visual conditioning, style control, or duration control
   until a controlled test proves it is used.
7. Promote only that backend to `experimental`; retain every other upstream as `planned`.
8. After reproducible smoke, evaluation, and release checks, consider `stable` according to the
   [research backend gate](research-backend-gate.md).

## Evidence Needed for the Grant Video

The application film can show a real generated comparison only after the above sequence yields:

- a valid `adapter.yaml` and model-registry entry under `config/model-registry/`;
- one authorized input project and its explicit output-distribution consent;
- accepted candidates produced by the actual adapter, not `opendub.test`;
- the generated WAV/MP4, `render.json`, candidate report, and run manifest from the same project;
- a signed item in the demo-film truth matrix.

Until then, use the alpha script and show architecture, authorization, timing workflow, and
planned model status without claiming a generated emotional or video-aware result.
