# Definition of Done

## Content Unit

A Method Manifest, Case or Replay Bundle is complete only when:

- it passes the v1 schema and semantic validator;
- all assets have relative paths, exact SHA-256 and media metadata;
- all claims have primary paper/source references;
- status follows evidence rules;
- public assets have rights evidence and reviewer;
- core method nodes have author/researcher approval;
- UI rendering and deep links are covered by tests.

## Task Explorer

- Video, Text and Reference Speech are independently selectable.
- Generated Speech and Dubbed Video are distinct outputs.
- the formal equation agrees with the natural-language task definition.
- one time cursor synchronizes media, tokens and signals.
- auto-tour can be interrupted, paused and replayed.
- desktop, tablet and mobile visual QA pass.
- it works with static build and no API.

## Method Canvas

- each of the three core methods has an approved full path from inputs to output.
- every core node provides problem, inputs, outputs, evidence and mode-aware signal slots.
- all graph edges are real information dependencies.
- selecting a node and pinning a signal are keyboard accessible.
- missing signals degrade to an explicit reason.
- Concept values are labelled Illustrative.
- React Flow canvas is nonblank and readable at target viewports.

## Comparison Lab

- public candidate tracks pass same-input gate.
- at most one candidate audio plays.
- switching preserves time within 50ms.
- equal listening-gain policy is visible.
- metrics compare only equal IDs, versions and preprocessing hashes.
- unavailable and not-applicable states are not replaced by zeros.
- blind listening hides method identity until explicit reveal.
- exported report contains hashes, modes and scope limitation.

## Live Method

- source commit, code license, weight terms and SHA-256 are recorded.
- adapter runs isolated without mutating global site-packages.
- real smoke test uses authorized media and creates target audio.
- run manifest records environment, inputs, parameters and output hash.
- VisualizationProvider outputs only genuine registered signals.
- a failed Live run cannot surface as Replay or Live success.

## Grant Film

- shot log includes commit, content-lock, route, case, mode and approval.
- every narration sentence has paper/source/test/run evidence.
- all media is rights-approved.
- all Concept/Replay/Live labels remain visible after edit.
- branch A/B selection matches comparison gate result.
- captions, video and audio pass final checks.
- exported files and evidence archive have checksums.

## Release `v0.1.0-atlas`

- all required `SCOPE_AND_SUCCESS.md` items have objective evidence.
- `make check`, content validation, web tests, build and Playwright pass.
- README, citations, license, model status and known limitations agree.
- no private paths, checkpoints, user content or tokens are committed.
- release tag, static artifact and film shot log identify the same commit.
