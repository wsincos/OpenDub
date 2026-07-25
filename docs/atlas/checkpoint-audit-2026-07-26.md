# Checkpoint Availability Audit

**Audit date:** 2026-07-26
**Purpose:** identify published upstream checkpoint candidates without promoting any to an OpenDub runtime or public Replay.

## Admission rule

An accessible file is not automatically an admissible checkpoint. OpenDub requires an immutable source commit, exact URL and filename, byte size, SHA-256 computed after acquisition, explicit weight-use terms, an isolated reproducible inference command, and an authorized input fixture. A public comparison further requires a shared Case Manifest and redistributable output rights.

## Findings

| Method | Source commit | Official README candidate | Availability check | Admission decision |
|---|---|---|---|---|
| EmoDubber / Chem basic function | `553fa054160fed17e757125d185e5a61ef6ed437` | Google Drive file ID `1CqTZU98xmHMy9C9Q0gFHvGyaZjUifizO` | 2026-07-26 unauthenticated `HEAD` reported `Emodubber_chem_1399.ckpt`, `1,233,766,000` bytes | **Candidate only**: no publisher SHA-256 or explicit weight-use terms; runtime needs precomputed features and a matched 16 kHz vocoder. Emotion-control inference remains under construction upstream. |
| EmoDubber / GRID basic function | `553fa054160fed17e757125d185e5a61ef6ed437` | Google Drive file ID `1RRf--kPzldhHro6jbauh2sP29iphIh-h` | Link published in README; not downloaded | **Candidate only**: same missing artifact and license evidence. |
| HPMDubbing / Chem | `f50dfa7df649208c674f151e52ad0a38d0b0bd43` | Google Drive file ID `1YCH2orTDmoKnTG8a5aaMQRv_QLjVTv-_` | 2026-07-26 download endpoint redirected to a Google sign-in flow | **Unavailable for automated admission**: no anonymous artifact retrieval, no SHA-256, no explicit weight terms. |
| HPMDubbing / V2C | `f50dfa7df649208c674f151e52ad0a38d0b0bd43` | Google Drive file ID `1EayaUNVHR21L3zAwG4X5WdVkoB5Fgjn0` | Link published in README; not downloaded | **Candidate only**: V2C source media has stated copyright constraints and cannot become a public OpenDub case without separate authorization. |
| StyleDubber / GRID | `bc431c8f67e885433c5c23163a8eaccb0dd41175` | Google Drive file ID `1ehSKyKw_UkKiNJCcupujcLAmyTtvxaEY` | 2026-07-26 unauthenticated `HEAD` reported `outout_GRID.zip`, `1,710,023,841` bytes | **Candidate only**: no publisher SHA-256 or explicit weight-use terms; requires dataset-specific precomputed phoneme-level features and matched acoustic configuration. |
| StyleDubber / V2C-Animation | `bc431c8f67e885433c5c23163a8eaccb0dd41175` | Google Drive file ID `1B3SIhActrdOEtVxktgW8K06_wf0GOeqN` | Link published in README; not downloaded | **Candidate only**: same missing artifact/license evidence; V2C material requires rights review. |

## Evidence sources

- EmoDubber official README: <https://github.com/GalaxyCong/EmoDubber>
- HPMDubbing official README: <https://github.com/GalaxyCong/HPMDubbing>
- StyleDubber official README: <https://github.com/GalaxyCong/StyleDubber>
- Fixed-source observations before this audit: `docs/audits/emodubber-553fa054.md`, `docs/audits/hpmdubbing-f50dfa7.md`, `docs/audits/styledubber-bc431c8.md`.

## What would change a decision

1. A project owner records a specific candidate's weight-use permission or receives written permission from the rights holder.
2. The file is manually acquired into a quarantined directory, its filename, byte size and SHA-256 are recorded, and the checksum is independently reviewed.
3. A disposable isolated environment produces a standard WAV from an authorized fixture without patching global site packages.
4. The fixture's video, text and reference-speech rights are recorded separately. It may not use restricted V2C source media.
5. The resulting run is packed as a private Replay Bundle first. It can enter the public Atlas only after display and redistribution review.

Until all five steps are complete, every frontend method remains `runtime_status=unavailable`, every public method page remains `Concept`, and the Comparison Lab remains evidence-gated.
