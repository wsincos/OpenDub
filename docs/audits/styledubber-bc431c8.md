# StyleDubber Upstream Audit

**Audit date:** 2026-07-25  
**Repository:** `https://github.com/GalaxyCong/StyleDubber`  
**Pinned commit:** `bc431c8f67e885433c5c23163a8eaccb0dd41175`  
**OpenDub status:** `planned`  
**Audit scope:** Source tree and published repository instructions only. No checkpoint was
downloaded, no dataset was accepted, and no inference result was claimed.

## Evidence

| Item | Finding | Evidence at pinned commit | OpenDub consequence |
|---|---|---|---|
| Source license | MIT | Root `LICENSE`, copyright 2024 Gaoxiang Cong | Source can be evaluated for an isolated adapter subject to notices. |
| Published scope | Training and inference scripts are present | Root README and `0_evaluate_*` scripts | A future adapter can begin from a published evaluation workflow rather than a webpage-only demo. |
| Input contract | Dataset-specific precomputed visual, face, text and audio features | README dataset trees; `dataset.py`; evaluation scripts | This is not a raw-video runtime. OpenDub needs a reproducible preprocessing pipeline and authorized fixtures. |
| Acoustic contract | README distinguishes StyleDubber from HPMDubbing and declares hop `256`, window `1024`, 22.05 kHz ground-truth audio | README dataset note | A future adapter/vocoder integration must validate mel configuration rather than infer it from file names. |
| Checkpoints | Google Drive and Baidu Drive links for GRID and V2C-Animation | README “Checkpoints” section | Links do not provide recorded artifact terms, byte size, or SHA-256; automatic download remains prohibited. |
| Evaluation | Published WER and speaker-similarity script instructions | README “Output Result” section | Upstream metrics depend on additional model downloads and data; OpenDub cannot inherit their results without independent runs. |
| Runtime | Python 3.8.18, CUDA 11.5, Torch 2.0.1 stated by upstream | README environment and `requirements.txt` | The core OpenDub package must not import this stack; a future adapter belongs in an isolated worker environment. |
| Style/emotion capability | Model source contains style and emotion-named classes, but no product-level capability contract was verified | `style_dubber/`, `evaluate.py` | No UI control, strength parameter, or output-quality claim may be enabled until an adapter proves accepted inputs and measurable behavior. |

## Release Gate

StyleDubber remains `planned`. Promotion to `experimental` requires:

1. explicit checkpoint terms, filename, SHA-256 and byte size;
2. an authorized GRID or V2C fixture with every required feature and a reproducible preprocessing record;
3. an isolated worker that produces standard WAV output without modifying global packages;
4. a declared input/output contract covering sample rate, hop length, window length, visual feature cadence and reference-audio requirements;
5. real smoke output and redacted manifest checks in CI;
6. a capability test showing any exposed style or emotion parameter changes the actual adapter input and output.

Until those conditions hold, StyleDubber is a research foundation and a planned upstream adapter,
not a selectable OpenDub backend.

