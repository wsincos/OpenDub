#!/usr/bin/env bash
# Build the caption-led V2 showcase from recorded browser interactions and approved example media.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
video_dir="$root/docs/grant/video/v2"
assets="$video_dir/assets/screens"
clips="$video_dir/assets/clips"
work="$video_dir/.work"
font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
output="$video_dir/OpenDub_VTTS_Showcase_v2.0.0.mp4"

mkdir -p "$work"

no_speech_bed="aevalsrc=0.010*sin(2*PI*110*t)+0.005*sin(2*PI*173*t)+0.002*sin(2*PI*0.17*t)*sin(2*PI*440*t):s=48000:c=stereo"

make_still() {
  local name="$1"
  local seconds="$2"
  local image="$3"
  ffmpeg -y -v error -loop 1 -framerate 30 -t "$seconds" -i "$image" \
    -f lavfi -t "$seconds" -i "$no_speech_bed" \
    -vf "scale=1980:1114,crop=1920:1080:x=(in_w-out_w)/2:y=(in_h-out_h)/2,format=yuv420p" \
    -map 0:v -map 1:a -c:v libx264 -preset medium -crf 18 -r 30 \
    -c:a aac -ar 48000 -b:a 128k -shortest "$work/$name.mp4"
}

make_browser_clip() {
  local name="$1"
  local source="$2"
  local seconds="$3"
  # Playwright begins recording before the first application paint; discard that blank transition.
  ffmpeg -y -v error -ss 0.5 -i "$source" -f lavfi -t "$seconds" -i "$no_speech_bed" \
    -filter_complex "[0:v]fps=30,scale=1980:1114,crop=1920:1080:x=(in_w-out_w)/2:y=(in_h-out_h)/2,drawbox=x=28:y=1022:w=556:h=34:color=0x101617@0.88:t=fill,drawtext=fontfile=$font:text='CAPTION-LED EXPLANATION / NON-SPEECH AUDIO':fontcolor=0xa7daca:fontsize=17:x=45:y=1030,format=yuv420p[v]" \
    -map "[v]" -map 1:a -t "$seconds" -c:v libx264 -preset medium -crf 18 -r 30 \
    -c:a aac -ar 48000 -b:a 128k -shortest "$work/$name.mp4"
}

make_human_grid() {
  ffmpeg -y -v error -stream_loop -1 -i "$root/apps/web/public/showcases/v2/human-0/gt.mp4" \
    -stream_loop -1 -i "$root/apps/web/public/showcases/v2/human-0/hpmdubbing.mp4" \
    -stream_loop -1 -i "$root/apps/web/public/showcases/v2/human-0/styledubber.mp4" \
    -stream_loop -1 -i "$root/apps/web/public/showcases/v2/human-0/emodubber.mp4" \
    -filter_complex "\
      [0:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='GT / Ground truth':fontcolor=0x8bd5c0:fontsize=26:x=25:y=15[a];\
      [1:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='METHOD / HPMDubbing':fontcolor=0xf0b967:fontsize=26:x=25:y=15[b];\
      [2:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='METHOD / StyleDubber':fontcolor=0xf0b967:fontsize=26:x=25:y=15[c];\
      [3:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='METHOD / EmoDubber':fontcolor=0xf0b967:fontsize=26:x=25:y=15[d];\
      [a][b]hstack=inputs=2[top];[c][d]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2,drawbox=x=0:y=1022:w=1920:h=58:color=0x101617@0.90:t=fill,drawtext=fontfile=$font:text='ARCHIVED RESEARCH EXAMPLE / human-0 / AUDIBLE: GT / Not a fresh OpenDub run':fontcolor=0xe6eeeb:fontsize=24:x=35:y=1037[v]" \
    -map "[v]" -map 0:a -t 12 -c:v libx264 -preset medium -crf 18 -r 30 \
    -c:a aac -ar 48000 -b:a 128k "$work/04-human-grid.mp4"
}

make_animation_grid() {
  ffmpeg -y -v error -stream_loop -1 -i "$root/apps/web/public/showcases/v2/animation-1/gt.mp4" \
    -stream_loop -1 -i "$root/apps/web/public/showcases/v2/animation-1/hpmdubbing.mp4" \
    -stream_loop -1 -i "$root/apps/web/public/showcases/v2/animation-1/styledubber.mp4" \
    -stream_loop -1 -i "$root/apps/web/public/showcases/v2/animation-1/emodubber.mp4" \
    -filter_complex "\
      [0:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='GT / Ground truth':fontcolor=0x8bd5c0:fontsize=26:x=25:y=15[a];\
      [1:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='METHOD / HPMDubbing':fontcolor=0xf0b967:fontsize=26:x=25:y=15[b];\
      [2:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='METHOD / StyleDubber':fontcolor=0xf0b967:fontsize=26:x=25:y=15[c];\
      [3:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,drawbox=x=0:y=0:w=960:h=52:color=0x101617@0.86:t=fill,drawtext=fontfile=$font:text='METHOD / EmoDubber':fontcolor=0xf0b967:fontsize=26:x=25:y=15[d];\
      [a][b]hstack=inputs=2[top];[c][d]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2,drawbox=x=0:y=1022:w=1920:h=58:color=0x101617@0.90:t=fill,drawtext=fontfile=$font:text='ARCHIVED RESEARCH EXAMPLE / animation-1 / AUDIBLE: GT / Not a fresh OpenDub run':fontcolor=0xe6eeeb:fontsize=24:x=35:y=1037[v]" \
    -map "[v]" -map 0:a -t 10 -c:v libx264 -preset medium -crf 18 -r 30 \
    -c:a aac -ar 48000 -b:a 128k "$work/05-animation-grid.mp4"
}

make_browser_clip "01-task-flow" "$clips/01-task-flow.webm" 7.5
make_browser_clip "02-cues" "$clips/02-cue-microscope.webm" 5
make_browser_clip "03-timeline" "$clips/03-shared-timeline.webm" 7.5
make_human_grid
make_animation_grid
make_still "06-methods" 11 "$assets/05-methods.png"
make_still "07-emodubber" 11 "$assets/06-emodubber.png"
make_still "08-evidence" 10 "$assets/07-evidence.png"
make_still "09-close" 10 "$assets/01-task-flow.png"

printf "file '%s'\n" "$work/01-task-flow.mp4" "$work/02-cues.mp4" "$work/03-timeline.mp4" \
  "$work/04-human-grid.mp4" "$work/05-animation-grid.mp4" "$work/06-methods.mp4" \
  "$work/07-emodubber.mp4" "$work/08-evidence.mp4" "$work/09-close.mp4" > "$work/concat.txt"

ffmpeg -y -v error -f concat -safe 0 -i "$work/concat.txt" -i "$video_dir/OpenDub_VTTS_Showcase_v2.0.0_CN_EN.srt" \
  -map 0:v -map 0:a -map 1:0 -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 128k \
  -c:s mov_text -metadata:s:s:0 language=chi -metadata:s:s:0 title="Chinese and English captions" \
  -movflags +faststart "$output"

ffmpeg -y -v error -i "$output" -vf "fps=1/11,scale=480:-1,tile=5x2" -frames:v 1 "$video_dir/contact-sheet.png"
python3 "$root/scripts/update_v2_video_manifest.py" --video-dir "$video_dir"
(cd "$video_dir" && sha256sum "$(basename "$output")" > "OpenDub_VTTS_Showcase_v2.0.0.sha256")
