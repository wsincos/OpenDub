# Three-Method Interactive Experience Specification

**Purpose:** define the exact public interaction and content boundary for HPMDubbing, StyleDubber and EmoDubber.
**Use this with:** `CORE_METHODS.md` for paper-level method facts and `VISUALIZATION_SIGNAL_MAP.md` for signal provenance rules.

## 1. Shared method-page contract

Every `/methods/:methodSlug` page has six fixed regions. The layout stays consistent so a visitor can learn the interface once, while the visual explanation remains method-specific.

| Region | Job | Mandatory content | Must not do |
|---|---|---|---|
| identity rail | establish what complete method is open | paper title, venue/year, research question, status, paper/source/citation actions | imply it is a reusable submodule |
| flow canvas | show real information dependencies | named components, typed edges, input/output direction | show arbitrary layers merely to fill the canvas |
| inspector | answer why a selected component exists | problem, inputs, outputs, relation, paper anchor, content status | claim hidden tensors not exported by paper/code |
| concept lab | make the paper's most distinctive idea interactive | one method-specific control and a textual interpretation | make a control sound like a new inference run |
| signal dock | preserve time-aligned evidence when available | pinning slots, provenance and unavailable state | fill absent signals with random plots |
| evidence footer | make every claim traceable | paper, code, commit, license, content/runtime state | hide missing checkpoint terms |

### States

Each region receives a `mode` from the content manifest:

| Mode | User sees | Data requirement | Interaction limit |
|---|---|---|---|
| `Concept` | paper-grounded relationships and explicitly illustrative graphics | approved method manifest and primary-source anchors | controls explain relationships only |
| `Replay` | approved historical assets and time-synchronized playback | rights record, hashes and run/source metadata | controls select recorded variants only |
| `Live` | current run output and registered artifacts | admitted adapter, checkpoint and run manifest | controls may submit a real run |
| `Planned` | route-map capability and missing prerequisite | roadmap record | no audio, metrics or animated data claim |

The mode is part of the visual composition, not a small footnote: it appears in the identity rail, inspector and any audio/output area.

## 2. HPMDubbing: Hierarchical Prosody Lens

### The message to communicate

> Different visual scales contribute different prosodic constraints: lips constrain local timing, the face informs local pitch/energy expression, and the scene contributes broader emotional context.

### Complete path to draw

```text
Target text -> phonemes ------------------------------------+
Reference speech -> speaker information --------------------+---> acoustic representation
Lip motion -> duration/alignment ---------------------------+
Face features -> valence/arousal -> pitch and energy -------+
Scene features -> global emotion ---------------------------+
                                                                  |
                                                                  v
                                                          mel spectrogram
                                                                  |
                                                                  v
                                                               vocoder
                                                                  |
                                                                  v
                                                           target speech
```

The final vocoder stage is supporting infrastructure inside the complete method flow, not a separate selectable method.

### Required nodes and inspector answers

| Node | Inspector question | Typed output | Concept interaction |
|---|---|---|---|
| Lip Motion | How does visible articulation constrain timing? | duration/alignment condition | choose `Lip motion` and show lip crop -> phoneme duration relationship |
| Face Affect | How do facial expressions affect local delivery? | valence/arousal, pitch/energy condition | choose `Face affect` and highlight F0/energy explanation |
| Scene Emotion | Why is a global scene cue separate from a face cue? | global emotion condition | choose `Scene affect` and highlight utterance-level context |
| Hierarchical Prosody | Where do the three visual roles meet? | prosody-conditioned acoustic representation | show converging lines, not fabricated attention weights |
| Mel Decoder | How does the acoustic representation become a spectral target? | mel spectrogram | show provenance-aware mel slot |
| Vocoder | How does a mel target become speech? | waveform | show output-stage relation |

### Interaction script

1. The visitor opens `Hierarchy lens`; Lip motion is active by default.
2. The line `Lip motion -> duration / local timing` is emphasized and a concise caption appears.
3. Clicking Face affect fades the other conceptual layers and changes the explanation to `Face affect -> pitch + energy / local expression`.
4. Clicking Scene affect changes it to `Scene affect -> global emotion / utterance context`.
5. Pinned signals, when a Replay/Live bundle exists, use the same time cursor: lip crop, phoneme interval, duration bar, F0 and energy.

### Asset contract

| Asset | Concept minimum | Replay/Live upgrade |
|---|---|---|
| scene/face/lip frame | self-created or rights-cleared still crop; `Illustrative` when not from a run | frame PTS plus ROI metadata |
| phoneme interval | typed illustrative token/range | token start/end time from replay/run |
| duration/F0/energy | labelled illustrative curve only | units, hop, source file and hash |
| mel/waveform | structural empty state or explicit illustrative sample | actual generated target speech and spectral metadata |

## 3. StyleDubber: Multi-scale Alignment Lens

### The message to communicate

> Style cannot be explained only at a video-frame scale. The method makes phoneme-scale alignment explicit while also preserving utterance-level style.

### Complete path to draw

```text
Target text -> phonemes -------------------------------------+
Reference speech + facial/video features --------------------+--> MPA
Lip motion + phonemes ---------------------------------------+--> PLA
MPA + PLA ----------------------------------------------------> intermediate embeddings
intermediate embeddings -------------------------------------> USL
                                                               |
                                                               v
                                                    mel decoder + refinement
                                                               |
                                                               v
                                                         target speech
```

### Required nodes and inspector answers

| Node | Inspector question | Typed output | Concept interaction |
|---|---|---|---|
| Phoneme View | Why is a script represented as intervals rather than one caption? | ordered phoneme sequence | switch from frame grid to phoneme intervals |
| MPA | How are reference pronunciation/style and visual cues used locally? | phoneme-level style representation | show three inputs converging at selected interval |
| PLA | How are lip movements associated with phonemes? | aligned phoneme representation | reveal lip-frame group behind selected phoneme |
| USL | What is preserved across the full utterance? | utterance-level style condition | shade a single phrase-wide style band |
| Mel Decoder | What acoustic target is produced? | mel spectrogram | reserve a source-aware spectrum panel |
| Refinement | What distinguishes a refined result stage? | refined mel / output | only compare pre/post plots with provenance |

### Interaction script

1. `Frame scale` is the default; six stable frame blocks are visible.
2. Selecting `Phoneme scale` reorganizes the same time extent into grouped phoneme intervals.
3. Clicking a phoneme interval highlights exactly its associated frame blocks and labels the local source ranges.
4. A persistent global style band shows why USL cannot be reduced to an isolated phoneme interaction.
5. If real assets are absent, the interface says `Conceptual interval map; not an exported attention matrix.`

### Asset contract

| Asset | Concept minimum | Replay/Live upgrade |
|---|---|---|
| frame/phoneme map | hand-authored interval geometry linked to paper concept | PTS, token boundaries and alignment metadata |
| reference voice | no public voice needed to explain a map | rights-cleared audio, selected range and hash |
| local/global style display | labelled relationship diagram | an approved exported representation with projection method |
| refined mel | absent or illustration only | actual pre/post spectral files and shared axes |

## 4. EmoDubber: Emotion Guidance Lens

### The message to communicate

> The method combines synchronization and pronunciation modeling with an explicit user request for emotion type and intensity, then guides generation toward the requested emotion and away from others.

### Complete path to draw

```text
Lip motion + phoneme prosody ------------> LPA -----+
Video-level phoneme sequence ------------> PE ------+--> fused sequence
Reference speech ------------------------> speaker identity adapting -> acoustic prior
Requested emotion type + intensity -----------------> FUEC / PNGM
acoustic prior -------------------------------------> FUEC / PNGM
                                                          |
                                                          v
                                                   target speech waveform
```

### Required nodes and inspector answers

| Node | Inspector question | Typed output | Concept interaction |
|---|---|---|---|
| LPA | How is lip movement related to phoneme prosody? | aligned sequence | expose timing relationship only |
| PE | How is pronunciation quality modeled beside synchronization? | enhanced phoneme sequence | show complete ordered phoneme path |
| Speaker Identity | Where does the requested voice identity enter? | acoustic prior | show reference-input dependency |
| Emotion Control | What may a user request? | categorical emotion + intensity | segmented emotion control and range control |
| FUEC | How is generation conditioned by acoustic and emotion signals? | output-generation trajectory/condition | structural, mode-labelled flow explanation |
| PNGM | What does positive/negative guidance mean? | direction and strength of guidance | opposing guidance rails with an interpretation |

### Interaction script

1. `Warm` is initially selected and the intensity starts at a visible numeric value.
2. Switching emotion changes the selected control and the explanatory labels, not an audio player.
3. Moving intensity updates a textual percentage and the relative emphasis of positive/negative guidance lines.
4. A persistent boundary statement reads: `No new audio generated in Concept mode.`
5. Only an exact recorded variant may enable playback for a changed setting; only an admitted run may enable a run button.

### Asset contract

| Asset | Concept minimum | Replay/Live upgrade |
|---|---|---|
| emotion type/intensity | declared categories and static guide relation | exact setting in replay/run manifest |
| guidance display | conceptual positive/negative diagram | explicitly exported approved signal, if available |
| target speech | no fabricated audio | authorized replay output or current run output |
| control efficacy | no claim | pre-registered control evaluation or clearly labelled user study result |

## 5. Cross-method comparison: permitted and forbidden mappings

| Shared research question | HPMDubbing | StyleDubber | EmoDubber | UI rule |
|---|---|---|---|---|
| lip-timing relation | lip motion -> duration | PLA | LPA | place on a research map; do not connect modules |
| phoneme representation | phoneme/acoustic path | MPA/PLA | PE | explain scope, not identical tensors |
| reference identity/style | speaker information | MPA + USL | speaker identity adapting | state method-specific role |
| visual emotion | face + scene hierarchy | video/facial style cues | user control plus visual sequence | distinguish inferred versus requested emotion |
| output stage | mel then vocoder | mel + refinement | flow/guided waveform path | never claim equal latency or quality without same-input evidence |

The compare page is unlocked only for valid common-input replay/live bundles. Until then, this mapping lives in the Method Atlas as a navigational explanation, not an empirical result table.

## 6. Per-method completion checklist

For each method, do not call the page complete until all items below have evidence:

- [ ] Paper title, venue/year, authorship and URLs checked against the primary paper.
- [ ] Source repository and fixed source revision recorded.
- [ ] All core node labels, edges and descriptions reviewed by a method owner.
- [ ] Method-specific Concept Lab interaction is keyboard accessible and its state is textually exposed.
- [ ] Concept graphics contain no hidden claim of Replay or Live data.
- [ ] Every unavailable replay/live signal has an explicit missing-evidence state.
- [ ] Paper and source actions are functional links; citation action is copyable.
- [ ] Desktop, tablet and mobile screenshots show no clipped content or graph overlap.
- [ ] Page tests cover selecting a node, using the unique Concept control and rendering the status boundary.
