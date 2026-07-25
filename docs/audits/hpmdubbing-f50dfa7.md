# HPMDubbing And Vocoder Upstream Audit

**Audit date:** 2026-07-25  
**HPMDubbing commit:** `f50dfa7df649208c674f151e52ad0a38d0b0bd43`  
**HPMDubbing_Vocoder commit:** `872251c6700f0e11de2e29741b2a29ca752b682d`  
**OpenDub status:** both `planned`

## HPMDubbing

| Item | Finding | OpenDub consequence |
|---|---|---|
| Source license | MIT | The source can be evaluated behind a separate worker environment. |
| Visual condition | The README describes lip, face, scene, valence/arousal features and inference scripts | A future adapter needs deterministic raw-video preprocessing; the public inference path is feature-file based. |
| Data constraints | V2C source movie frames are not public because of copyright; public links point to preprocessed data | OpenDub examples and release tests cannot use V2C assets unless independently authorized. |
| Runtime | Requirements pin Torch 1.8.1 + CUDA 11.1 and older scientific packages | It must remain outside the core environment and be installed only in an isolated adapter environment. |
| Checkpoints | Google Drive/Baidu Drive links are documented | No published SHA-256, byte size, immutable artifact URL, or weight-license evidence is recorded. |
| Raw project paths | README examples include absolute local paths and manual configuration replacement | A future adapter must construct a redacted manifest and never inherit upstream hard-coded paths. |

## HPMDubbing Vocoder

| Item | Finding | OpenDub consequence |
|---|---|---|
| Source license | MIT | Candidate for a separately licensed adapter after artifact validation. |
| Published contracts | `HPM_Chem`: 16,000 Hz, hop 160, win 640; `HPM_V2C`: 22,050 Hz, hop 220, win 880 | These must be encoded as explicit compatibility checks, never inferred from a filename. |
| Inference interface | `inference_e2e.py` is documented as mel-to-waveform | A future adapter can expose a narrow mel-to-WAV contract. |
| Checkpoints | Google Drive links for `g_05000000` generator checkpoints | The links lack recorded SHA-256 and explicit weight terms; automatic download is forbidden. |

## Release Gate

Neither component can advance from `planned` until an authorized artifact has a fixed
URL, hash, terms, and a real smoke test. HPMDubbing additionally requires an authorized
video/feature fixture. The Vocoder additionally requires a test that rejects every mel
whose sample rate, hop length, or mel-bin count differs from its selected contract.
