# HDCode Source Audit: `d088398`

**Audit date:** 2026-07-25  
**Scope:** source inventory only. This record is not a grant to redistribute datasets, checkpoints,
vocoder weights, or film media.

## Evidence Captured

| Field | Recorded value |
| --- | --- |
| Repository | `https://github.com/HD-Dub/HDCode` |
| Immutable source | `d08839848cf17805bb598abf468968f8fc7a28f7` |
| Source license | MIT, root `LICENSE`, copyright Liang Li (2021) |
| Published purpose | Hierarchical phoneme modeling and acoustic diffusion denoising for movie dubbing |
| Declared audio rate | 22050 Hz for data and features |
| Runtime entry points | `Inference_Runit.py` and `Inference_Runit_Setting2.py` |
| Declared legacy dependency | `torch==1.8.1` in `requirements.txt` |

## Admission Findings

The source tree provides training and inference scripts, which makes HDCode a useful future
adapter candidate for OpenDub's visual-sync and acoustic-generation capability. It must remain
isolated from the OpenDub core because its declared dependency set is legacy and its source
workflow is research-oriented.

The README currently marks preprocessed features and the CHEM, GRID, and V2C-Animation
checkpoints as not uploaded. It links to a 22050 Hz HiFi-GAN vocoder, but does not record terms,
artifact version, file size, or SHA-256. The audit did not download any weights or data and did not
perform inference.

## Promotion Gate

Do not register a user-facing HDCode adapter until all of the following are present:

1. A permitted checkpoint and, if needed, vocoder with explicit terms, immutable URL/version, and
   SHA-256.
2. A redistributable or explicitly authorized fixture that satisfies the published 22050 Hz feature
   contract without restricted movie media.
3. A pinned isolated runtime, an OpenDub JSON Lines adapter, and a real end-to-end smoke result.
4. Artifact provenance, output validation, known limitations, and a control-effect evaluation in
   the model card.

Until then, registry maturity is `planned`; it must not be represented in Studio or in the grant
film as a runnable model.
