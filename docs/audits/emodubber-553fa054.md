# EmoDubber Upstream Audit

**Audit date:** 2026-07-25  
**Repository:** `https://github.com/GalaxyCong/EmoDubber`  
**Pinned commit:** `553fa054160fed17e757125d185e5a61ef6ed437`  
**OpenDub status:** `planned`  
**Audit scope:** Source tree and published repository instructions only. No external
checkpoint was downloaded, and no inference result was claimed.

## Evidence

| Item | Finding | Evidence at pinned commit | OpenDub consequence |
|---|---|---|---|
| Source license | MIT | Root `LICENSE`, copyright 2025 Gaoxiang Cong | Source can be evaluated for an isolated adapter subject to notices. |
| Basic inference | Present | `EmoDubber_Networks/Inference_*` scripts; README documents Chem/GRID inference arguments | A future basic adapter can target the published feature-file workflow. |
| Video input contract | Precomputed lip and face features | README requires `Silent_Lip`, `Silent_Face`, reference-audio features, plus a file list | It is not a raw-video, plug-and-play runtime; OpenDub needs deterministic preprocessing adapters. |
| Basic checkpoints | Linked through Google Drive/Baidu Drive | README "Our Checkpoints" section | Links are not immutable artifact URLs and publish no SHA-256 or explicit weight license. |
| Vocoder | 16 kHz checkpoint linked | README inference section; `Vocoder_16KHz/` | Must be separately pinned, hashed, license-reviewed, and compatibility-tested. |
| Emotion labels / strength | Not releasable in this commit | README TODO lists emotion controlling code as unfinished; "Emotion Controlling / Inference: Under construction" | `supports_emotion_strength` and all emotion-control claims remain unavailable. |
| Metrics | Not fully released | README TODO marks metrics scripts unfinished | No upstream quality claim can be imported into OpenDub without independent verification. |
| Runtime isolation | Python 3.10, Torch/Lightning dependency stack | README environment steps and `requirements.txt` | Must run outside the core environment via the JSON Lines adapter runtime. |
| Site-packages patch | Suggested only for training | README describes replacing two Lightning package files, then says inference should ignore it | OpenDub must not require this patch; a future adapter has to prove an unmodified inference path. |

## Release Gate

The upstream record remains `planned`. It may advance to `experimental` only after all
of the following are recorded in `model-registry/upstreams.yaml` and verified in CI:

1. an authorized checkpoint URL, exact filename, byte size, SHA-256, and weight terms;
2. a reproducible, unmodified inference environment and command at the pinned commit;
3. an authorized input fixture that produces a standard WAV through an isolated worker;
4. a capability manifest that declares only controls demonstrably accepted and used;
5. a smoke-test artifact with input/output hashes and a redacted run manifest.

Emotion direction is a separate gate. It requires published inference code, a
reproducible weight set, and a metric or controlled comparison showing that the
declared control changes output. Until then, OpenDub must render the backend as
`Planned adapter`, not as an enabled emotion feature.

## Attribution

OpenDub does not claim EmoDubber's method as original platform work. Any eventual
adapter and model card must cite the upstream repository and the paper named in its
README.
