# Planned Research Backends

These records are intentionally separate from runnable adapter configuration. Their authoritative
machine-readable status is `planned` in `../upstreams.yaml`; this directory is a review index, not a
weight download location.

| Backend | Current evidence boundary | Promotion blocker |
| --- | --- | --- |
| EmoDubber | MIT source and a fixed source audit | Weight terms/hash and verified emotion inference |
| HPMDubbing | MIT source and feature-workflow audit | Authorized raw-video fixture and reproducible preprocessing |
| StyleDubber | MIT source and feature-contract audit | Weight terms/hash and isolated real inference |
| HPMDubbing Vocoder | MIT source and declared mel contracts | Weight terms/hash and acoustic compatibility smoke |
| HDCode | MIT source, fixed commit, 22.05 kHz declared contract | Published checkpoint/feature evidence and isolated smoke |
| CoSyncDiT | Project description only | Usable code, weights, license, contract, and smoke |
| LLM-Flow-Dubber | Static demonstration site | Model implementation, weights, license, contract, and smoke |

Use the promotion packet in
[`docs/adapters/research-backend-gate.md`](../../../docs/adapters/research-backend-gate.md) before
changing any entry to `experimental` or `stable`.
