# V2 Showcase Controlled Source-Evidence Register

**Register date:** 2026-07-27
**Record owner:** OpenDub project owner / repository maintainer
**Verification contact:** `wsincos1025@gmail.com`
**Applies to:** the restricted local source files named by the two manifests in `apps/web/content/showcases/v2/`

## Purpose and public boundary

This register makes the V2 showcase source chain reviewable without publishing the underlying source videos, reference speech, or identifying metadata. It supplements the public [V2 showcase media authorization record](showcase-media-rights-v2.md); it is not a public dataset card, a benchmark license, or a Replay contract.

Anyone may verify the bytes that are publicly shipped in `apps/web/public/showcases/v2/`, their derived features, and the corresponding manifest hashes. Verification of the restricted source files is available only through the project maintainer, because the source files are deliberately excluded from version control and redistribution. The public cases remain `Archived research example` and must never be described as a same-input benchmark, `Replay`, `Live` result, or newly generated OpenDub output.

## Controlled source index

The following SHA-256 values are the approval anchors for the exact restricted source files. `source identifier` is intentionally a stable, non-identifying verification label rather than a public filesystem path or a claim about an upstream dataset.

| Case | Source identifier | Display artifact | SHA-256 | Approval scope |
| --- | --- | --- | --- | --- |
| `human-0` | `human-0/ground-truth` | `gt.mp4` | `a0860898765540b2e615d7f5784b20391fa7b2ef5c2957277e0cc2a302c380bb` | Repository display and seed-plan application material only |
| `human-0` | `human-0/hpmdubbing-output` | `hpmdubbing.mp4` | `8d3524b7caeec9ff854357ba9773bf01170c869c7f418ec03fc35c1f123d2bd9` | Repository display and seed-plan application material only |
| `human-0` | `human-0/styledubber-output` | `styledubber.mp4` | `c5869d3d6840315ee66042070a8a09c7a6ff7876bcbcfb4f1b0efc37d0a94199` | Repository display and seed-plan application material only |
| `human-0` | `human-0/emodubber-output` | `emodubber.mp4` | `7a871e0323ff8f32643a9d3e956180e4e231dc64fb192911f9fc822d763ad302` | Repository display and seed-plan application material only |
| `animation-1` | `animation-1/ground-truth` | `gt.mp4` | `ade15d9a93fe060d40b20931c75b7f9ac68cff8a54c35ffac259e4edaaab50b3` | Repository display and seed-plan application material only |
| `animation-1` | `animation-1/hpmdubbing-output` | `hpmdubbing.mp4` | `b07f33292ad3de2ed44d58388b69aef51d6a267b6f7ba7b18ba0557f99d0cc49` | Repository display and seed-plan application material only |
| `animation-1` | `animation-1/styledubber-output` | `styledubber.mp4` | `8142dcf5f3799554ff5c586ce6e29cfedf81e042a54f73aec25925107b18aaf2` | Repository display and seed-plan application material only |
| `animation-1` | `animation-1/emodubber-output` | `emodubber.mp4` | `73af4ad278d19bfeb3bb650edc8c00ba89a9ee986e103f3e6c56390e52574f2a` | Repository display and seed-plan application material only |

## Approval, access, and revocation

- **Approver:** OpenDub project owner / repository maintainer.
- **Approval date:** 2026-07-27.
- **Permitted scope:** the exact hashed files, their public display copies, poster frames, audio-derived waveform/F0/energy/log-mel features, and the corresponding segments in the OpenDub seed-plan material.
- **Excluded scope:** raw-source redistribution, identity/voice reuse, training-data release, benchmark reuse, model-weight distribution, and any claim that the records form a common-input comparison contract.
- **Controlled verification:** an applicant reviewer, rights holder, or maintainer may request hash-to-source confirmation through the verification contact above. The request must identify the case ID and artifact name; the maintainer may verify the requested hash and approval record without transferring the restricted media.
- **Withdrawal or conflict:** the maintainer must remove the affected public media, derivative assets, and application-video segment; mark the case `blocked`; and update the manifest, authorization record, and release notes. The retained register entry documents why the prior display was removed, but it does not preserve the media.

## Relationship to the public package

The case manifests are the machine-readable source of truth for the public asset paths and hashes. The public `provenance.json` files prove that the displayed copies and audio-derived features bind to those hashes. This register adds the controlled source identifiers and approval channel that a clean clone cannot contain. Together, these records provide a constrained exhibition trail, not a third-party copyright audit or a fully public reproduction chain.
