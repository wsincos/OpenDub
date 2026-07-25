# CNN Visualization Reference Translation

`reference/CNN.txt` contains examples such as CNN Explainer, TensorFlow Playground, ConvNetJS, Distill, TensorBoard Graph and OpenAI Microscope. OpenDub should borrow their interaction principles, not copy their visual forms.

| Reference principle | OpenDub translation | Explicit boundary |
|---|---|---|
| CNN Explainer: click a layer to inspect its input/output | click a Method Canvas node to inspect its problem, signals and paper evidence | a method node is not automatically a single neural layer |
| TensorFlow Playground: change a control and see consequences | Emo control can change a matching Replay or Live result | no synthetic audio is presented as newly generated |
| Distill: explain one idea at a time | Task Explorer introduces Video, Text, Voice, then Method | no dense all-at-once architecture poster |
| TensorBoard Graph: navigate a large directed graph | React Flow shows complete method information flow | only semantic paper edges, no meaningless tensor wiring |
| OpenAI Microscope: inspect model internals | inspect exported/approved Lip, phoneme, prosody, mel and waveform signals | no unsupported activation maps or attention views |
| Interactive timeline | one playhead binds video, tokens, prosody and output | internal non-temporal tensors are not falsely tied to time |

## Design Rule

Every interaction must answer one of four questions:

1. What constraint does this input contribute?
2. What problem does this component solve?
3. What observable evidence supports that claim?
4. Is this a Concept, Replay, Live or Planned view?

If an interaction cannot answer one of these, it does not belong in the first release.
