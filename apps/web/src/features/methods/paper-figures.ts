import type { MethodDefinition } from "../../content/methods";

export type PaperFigureRegion = {
  detail: string;
  id: string;
  label: string;
  x: number;
  y: number;
  width: number;
  height: number;
};

export type PaperFigureDefinition = {
  caption: string;
  imagePath: string;
  regions: PaperFigureRegion[];
};

const paperFigures: Record<MethodDefinition["id"], PaperFigureDefinition> = {
  "galaxycong/hpmdubbing": {
    imagePath: "/methods/papers/hpmdubbing-architecture.png",
    caption: "Original method architecture, published with the source record. Region markers are OpenDub reading aids, not live activations.",
    regions: [
      { id: "duration", label: "Duration Aligner", detail: "Phoneme and speaker conditions are aligned to establish duration before acoustic generation.", x: 2.1, y: 43.3, width: 20.4, height: 40.2 },
      { id: "prosody", label: "Prosody Adaptor", detail: "Lip and facial cues provide arousal and valence conditions that shape prosodic representation.", x: 27.8, y: 43.3, width: 20.5, height: 37.1 },
      { id: "atmosphere", label: "Atmosphere Booster", detail: "Scene features are fused through cross-attention to form a scene-aware prosody condition.", x: 53, y: 43.3, width: 20.07, height: 34.36 },
      { id: "acoustic", label: "Mel Generator", detail: "The complete condition is decoded into a mel-spectrogram before waveform synthesis by the vocoder.", x: 78.5, y: 43.3, width: 17.9, height: 31.3 },
    ],
  },
  "galaxycong/styledubber": {
    imagePath: "/methods/papers/styledubber-architecture.png",
    caption: "Original method architecture, published with the source record. Region markers are OpenDub reading aids, not live activations.",
    regions: [
      { id: "adapter", label: "Multimodal Adapter", detail: "Acoustic reference and visual emotion representations are aligned into a shared multimodal condition.", x: 6.46, y: 26.91, width: 72.82, height: 38.66 },
      { id: "lip", label: "Phoneme-guided Lip Aligner", detail: "Lip-motion features and phoneme timing guide the duration path used by the downstream decoder.", x: 64.2, y: 18.5, width: 31.6, height: 57.5 },
      { id: "style", label: "Utterance-level Style Learning", detail: "Utterance-scale style statistics complement local phoneme-level conditions.", x: 6.5, y: 67.92, width: 28.37, height: 26.22 },
      { id: "decoder", label: "Mel Decoder", detail: "The decoder and post-net transform the fused representation into the mel-spectrogram consumed by the vocoder.", x: 35.71, y: 66.2, width: 31.43, height: 28.34 },
    ],
  },
  "galaxycong/emodubber": {
    imagePath: "/methods/papers/emodubber-architecture.png",
    caption: "Original method architecture, published with the source record. Region markers are OpenDub reading aids, not live activations.",
    regions: [
      { id: "identity", label: "Speaker Identity Adapting", detail: "Reference-style identity is adapted into the acoustic prior used for the target speaker.", x: 2.8, y: 3, width: 56.77, height: 19.06 },
      { id: "prosody", label: "Lip-related Prosody Aligning", detail: "Lip representations are aligned with prosody conditions to support synchronized delivery.", x: 2.98, y: 26.2, width: 31.37, height: 44.07 },
      { id: "pronunciation", label: "Pronunciation Enhancing", detail: "A pronunciation-oriented branch reinforces phoneme clarity alongside the generated acoustic condition.", x: 35.59, y: 26.2, width: 22.59, height: 44.56 },
      { id: "emotion", label: "Flow-based User Emotion Controlling", detail: "A flow-based generator combines emotion direction and intensity guidance with the acoustic prior.", x: 60, y: 3, width: 37.2, height: 87.5 },
    ],
  },
};

export function getPaperFigure(method: MethodDefinition): PaperFigureDefinition {
  return paperFigures[method.id];
}
