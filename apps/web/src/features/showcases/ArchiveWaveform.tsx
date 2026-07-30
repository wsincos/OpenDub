import { useAudioFeature } from "../vtts/useAudioFeature";

type ArchiveWaveformProps = {
  color: string;
  featureUrl: string;
  label: string;
};

export function ArchiveWaveform({ color, featureUrl, label }: ArchiveWaveformProps) {
  const feature = useAudioFeature(featureUrl);
  const peaks = feature?.waveform_peaks ?? [];
  const maximumPeak = Math.max(...peaks, 0.00001);

  if (!peaks.length) {
    return <div aria-label={`${label} waveform`} className="archive-waveform archive-waveform-empty" role="img">AUDIO FEATURE UNAVAILABLE</div>;
  }

  return (
    <svg aria-label={`${label} waveform`} className="archive-waveform" height="37" preserveAspectRatio="none" role="img" viewBox="0 0 100 30" width="100%">
      {peaks.map((peak, index) => {
        const x = peaks.length === 1 ? 50 : index / (peaks.length - 1) * 100;
        const amplitude = Math.min(13, peak / maximumPeak * 13);
        return <line key={index} stroke={color} x1={x} x2={x} y1={15 - amplitude} y2={15 + amplitude} />;
      })}
    </svg>
  );
}
