#!/usr/bin/env bash
# Build the V3 narrated evidence walkthrough from real browser captures and approved audio sources.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
video_dir="$root/docs/grant/video/v3"
captures="$video_dir/assets/browser-captures"
audio_map="$video_dir/source-audio-map.json"
v1_video="$root/docs/grant/video/OpenDub_Application_Walkthrough_v0.0.1-alpha.0.mp4"
font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
output="$video_dir/OpenDub_Narrated_Evidence_Walkthrough_v3.0.0.mp4"
subtitle="$video_dir/OpenDub_Narrated_Evidence_Walkthrough_v3.0.0_CN_EN.srt"
work="$(mktemp -d /tmp/opendub-v3-film.XXXXXX)"

trap 'rm -rf "$work"' EXIT

"$root/.venv/bin/python" "$root/scripts/verify_v3_audio_map.py" "$audio_map" --root "$root" --require-captures

range_for() {
  local clip_id="$1"
  "$root/.venv/bin/python" - "$audio_map" "$clip_id" <<'PY'
import json
import sys

payload = json.load(open(sys.argv[1], encoding="utf-8"))
for item in payload["narration_clips"]:
    if item["clip_id"] == sys.argv[2]:
        print(item["source_range"])
        break
else:
    raise SystemExit(f"missing narration clip: {sys.argv[2]}")
PY
}

seconds_between() {
  local start="$1"
  local end="$2"
  local start_minute="${start%:*}"
  local start_second="${start#*:}"
  local end_minute="${end%:*}"
  local end_second="${end#*:}"
  echo $((10#$end_minute * 60 + 10#$end_second - 10#$start_minute * 60 - 10#$start_second))
}

make_narrated_clip() {
  local name="$1"
  local capture="$2"
  local narration_id="$3"
  local range
  range="$(range_for "$narration_id")"
  local start="${range%-*}"
  local end="${range#*-}"
  local seconds
  seconds="$(seconds_between "$start" "$end")"
  ffmpeg -y -v error -ss 0.50 -stream_loop -1 -i "$capture" -ss "$start" -t "$seconds" -i "$v1_video" \
    -filter_complex "[0:v]fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,format=yuv420p[v];[1:a]loudnorm=I=-16:TP=-1:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]" \
    -map "[v]" -map "[a]" -t "$seconds" -c:v libx264 -preset medium -crf 18 -r 30 -c:a aac -ar 48000 -b:a 160k -movflags +faststart "$work/$name.mp4"
}

make_archive_clip() {
  local clip_id="$1"
  local case_id="$2"
  local artifact_path="$3"
  local visual_source="$4"
  local audio_source="$5"
  local duration="2.25"
  local audio_file="${audio_source%%#*}"
  local boundary="ARCHIVED RESEARCH EXAMPLE | $case_id | NOT A FRESH OPENDUB RUN"
  # Browser recording begins before navigation; the active player appears at about 2 seconds.
  ffmpeg -y -v error -ss 2.00 -stream_loop -1 -i "$root/$visual_source" -stream_loop -1 -i "$root/$audio_file" \
    -filter_complex "[0:v]fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,drawbox=x=28:y=1020:w=870:h=36:color=0x101617@0.90:t=fill,drawtext=fontfile=$font:text='$boundary':fontcolor=0xe6eeeb:fontsize=16:x=44:y=1030,format=yuv420p[v];[1:a]loudnorm=I=-16:TP=-1:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]" \
    -map "[v]" -map "[a]" -t "$duration" -c:v libx264 -preset medium -crf 18 -r 30 -c:a aac -ar 48000 -b:a 160k -movflags +faststart "$work/$clip_id.mp4"
}

make_narrated_clip "01-identity" "$captures/01-identity-task-flow.webm" "identity"
make_narrated_clip "02-task-illustration" "$captures/02-task-illustration.webm" "task-illustration"

archive_rows="$work/archive-rows.txt"
"$root/.venv/bin/python" - "$audio_map" > "$archive_rows" <<'PY'
import json
import sys

payload = json.load(open(sys.argv[1], encoding="utf-8"))
for item in payload["archive_clips"]:
    print("|".join((item["clip_id"], item["case_id"], item["artifact_path"], item["visual_source"], item["audio_source"])))
PY

archive_names=()
while IFS='|' read -r clip_id case_id artifact_path visual_source audio_source; do
  make_archive_clip "$clip_id" "$case_id" "$artifact_path" "$visual_source" "$audio_source"
  archive_names+=("$clip_id")
done < "$archive_rows"

make_narrated_clip "11-complete-methods" "$captures/03-method-selection.webm" "complete-methods"
make_narrated_clip "12-method-canvas" "$captures/04-method-canvas.webm" "method-canvas"
make_narrated_clip "13-evidence-boundary" "$captures/05-evidence-boundary.webm" "evidence-boundary"
make_narrated_clip "14-closing" "$captures/01-identity-task-flow.webm" "closing"

concat_file="$work/concat.txt"
{
  printf "file '%s'\n" "$work/01-identity.mp4" "$work/02-task-illustration.mp4"
  for name in "${archive_names[@]}"; do printf "file '%s'\n" "$work/$name.mp4"; done
  printf "file '%s'\n" "$work/11-complete-methods.mp4" "$work/12-method-canvas.mp4" "$work/13-evidence-boundary.mp4" "$work/14-closing.mp4"
} > "$concat_file"

ffmpeg -y -v error -f concat -safe 0 -i "$concat_file" -i "$subtitle" \
  -map 0:v -map 0:a -map 1:0 -c:v libx264 -preset medium -crf 18 -c:a aac -ar 48000 -b:a 160k \
  -c:s mov_text -metadata:s:s:0 language=chi -metadata:s:s:0 title="Chinese and English captions" \
  -t 111.95 -movflags +faststart "$output"

ffmpeg -y -v error -i "$output" -vf "fps=1/14,scale=480:-1,tile=4x2" -frames:v 1 "$video_dir/contact-sheet.png"
"$root/.venv/bin/python" "$root/scripts/update_v3_video_manifest.py" --video-dir "$video_dir"
(cd "$video_dir" && sha256sum "$(basename "$output")" > "OpenDub_Narrated_Evidence_Walkthrough_v3.0.0.sha256")
