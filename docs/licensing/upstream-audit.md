# Upstream Audit

This document records the first reproducibility boundary for OpenDub adapters. It is a source inventory, not a redistribution grant. Full adapter admission requires a source commit, source-license review, model-weight terms, checksums, input/output contract, and a real-inference smoke test.

| Model | Fixed source commit | Source license | Current OpenDub state | Admission gap |
|---|---|---|---|---|
| EmoDubber | `553fa054160fed17e757125d185e5a61ef6ed437` | MIT | Planned | Verify released emotion-control path and weight terms |
| HPMDubbing | `f50dfa7df649208c674f151e52ad0a38d0b0bd43` | MIT | Planned | Automate preprocessing and audit restricted data |
| StyleDubber | `bc431c8f67e885433c5c23163a8eaccb0dd41175` | MIT | Planned | Verify inference inputs, weights, and isolated runtime |
| HPMDubbing_Vocoder | `872251c6700f0e11de2e29741b2a29ca752b682d` | MIT | Planned | Record mel contract and weight checksums |
| HDCode | `d08839848cf17805bb598abf468968f8fc7a28f7` | MIT | Planned | Features/checkpoints are marked unpublished; verify weight terms and runtime |
| CoSyncDiT | `adfc14b85590dccc52f3fa87432ea8e50ab36289` | Not yet verified | Planned | Await usable code, weight, and license evidence |
| LLM-Flow-Dubber | `7075d8c170ea10786fea306c7c311c3bdb74f04f` | Not yet verified | Planned | Public repository is not a model implementation |

No source in this table is copied into OpenDub by this audit. Each future adapter stores its own license record and patch notes.
## EmoDubber

- Pinned source: `553fa054160fed17e757125d185e5a61ef6ed437`.
- Source license: MIT, confirmed from the root `LICENSE`.
- Published scope: basic Chem/GRID feature-file inference and a linked 16 kHz
  vocoder checkpoint.
- Blocking gaps: published emotion inference is explicitly under construction;
  linked weights have no recorded terms, byte size, or SHA-256.
- OpenDub disposition: `planned`; detailed evidence and release gate are in
  [`docs/audits/emodubber-553fa054.md`](../audits/emodubber-553fa054.md).

## HPMDubbing And HPMDubbing_Vocoder

- Pinned source commits: `f50dfa7df649208c674f151e52ad0a38d0b0bd43` and
  `872251c6700f0e11de2e29741b2a29ca752b682d`.
- Source licenses: MIT, confirmed from both root `LICENSE` files.
- Blocking gaps: the published model and vocoder checkpoint links lack recorded
  terms and SHA-256; HPMDubbing's published workflow depends on feature data and
  includes V2C material subject to copyright restrictions.
- OpenDub disposition: both remain `planned`; detailed contracts and release
  gates are in [`docs/audits/hpmdubbing-f50dfa7.md`](../audits/hpmdubbing-f50dfa7.md).

## StyleDubber

- Pinned source: `bc431c8f67e885433c5c23163a8eaccb0dd41175`.
- Source license: MIT, confirmed from the root `LICENSE`.
- Published scope: dataset-specific training/evaluation scripts and checkpoint links for
  GRID and V2C-Animation; the stated workflow uses precomputed features and a 22.05 kHz,
  hop-256, window-1024 acoustic configuration.
- Blocking gaps: checkpoint terms, immutable hashes, authorized fixtures, reproducible raw-video
  preprocessing and an isolated real inference remain unverified.
- OpenDub disposition: `planned`; detailed evidence and promotion gate are in
  [`docs/audits/styledubber-bc431c8.md`](../audits/styledubber-bc431c8.md).

## HDCode

- Pinned source: `d08839848cf17805bb598abf468968f8fc7a28f7`.
- Source license: MIT, confirmed from the root `LICENSE`.
- Published scope: 22.05 kHz training and inference entry points for CHEM, GRID, and
  V2C-Animation; a linked 22.05 kHz HiFi-GAN vocoder.
- Blocking gaps: the README explicitly lists preprocessed features and three model checkpoints
  as not uploaded; the vocoder and any future checkpoints lack recorded terms, byte size, and
  SHA-256. No isolated real inference was performed.
- OpenDub disposition: `planned`; detailed evidence and promotion gate are in
  [`docs/audits/hdcode-d088398.md`](../audits/hdcode-d088398.md).
