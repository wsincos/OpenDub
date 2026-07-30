# Local Quick Start

This guide runs the currently implemented, local-only OpenDub experience. It lets you inspect a
complete method, carry that choice into a project, import authorized local inputs, and export a
versioned preparation record. It does not install or claim a real dubbing model.

## Prerequisites

- Linux or macOS with Python 3.11 through 3.13;
- FFmpeg and FFprobe on `PATH`;
- Node.js 20+ for the Web Studio;
- `uv` for Python dependencies and `pnpm` for the Web workspace.

## Install and verify

```bash
git clone https://github.com/wsincos/OpenDub.git
cd OpenDub
uv sync --all-groups
make check
npm exec --yes --package=pnpm@9.15.0 -- pnpm install --frozen-lockfile
make web-check
```

The Python core intentionally does not import PyTorch. Real model adapters will be installed
in isolated environments only after their source, weight, and license records pass review.

## Start a private workspace

Use a directory outside the repository for real projects and media:

```bash
uv run opendub init --workspace ~/.local/share/opendub
uv run opendub doctor --workspace ~/.local/share/opendub
uv run opendub serve --workspace ~/.local/share/opendub --port 8000
```

The API binds to `127.0.0.1` by default. Its interactive local reference is available at
`http://127.0.0.1:8000/api/docs`.

In another terminal, start the Studio:

```bash
VITE_OPENDUB_API_BASE=http://127.0.0.1:8000 \
  npm exec --yes --package=pnpm@9.15.0 -- pnpm --filter @opendub/web dev --port 5173
```

Open `http://127.0.0.1:5173` in a modern browser.

If port `5173` is already occupied, start Vite with another loopback port such as `5180` and open that address instead. The local API accepts Studio requests from `localhost` and `127.0.0.1` development ports only; it does not open the workspace to remote web origins.

## Local workflow

1. Open `http://127.0.0.1:5173/methods`, inspect a complete method, and choose **Prepare project**.
2. Create a local project; Studio stores the selected method, its fixed evidence revision, and its declared input contract.
3. Import a video and audio that you own or are authorized to use. For an audio voice reference, record the material source and speaker label.
4. Add dialogue with a target start/end time, language, voice reference, emotion direction, and intensity.
5. Record the current video and target-text authorization declarations, then export `opendub-preparation.json` from the selected-method panel.

The Studio will state that no listed research model is verified for a Live run until an adapter
has passed the model admission gate. Do not interpret a `Concept` or `planned` status as an
available generation backend. The preparation export is a reproducible handoff record, not an
audio-generation request.

## Command line basics

```bash
uv run opendub create "Authorized demo" --workspace ~/.local/share/opendub
uv run opendub list --workspace ~/.local/share/opendub
uv run opendub doctor --workspace ~/.local/share/opendub --json
```

Evaluate any stored candidate with deterministic timing and waveform checks. The emitted report
also records unavailable neural metrics rather than fabricating scores:

```bash
uv run opendub evaluate PROJECT_ID CANDIDATE_ID --workspace ~/.local/share/opendub --json
```

Once a verified adapter has produced candidate takes and a reviewer has explicitly accepted at
least one current take, render a local dubbing WAV and, when a source video exists, an MP4:

```bash
uv run opendub render PROJECT_ID --workspace ~/.local/share/opendub --mix-mode remove
```

`remove` replaces the original video audio; `duck` mixes it at a reduced level; `preserve` mixes
it at full level. The API exposes the same operation at `POST /api/v1/projects/{project_id}/renders`
and serves only the resulting fixed-name artifacts from the corresponding export revision.

## Troubleshooting

`opendub doctor` reports missing FFmpeg, an unwritable workspace, or registry issues without
reading user media into telemetry. If the browser cannot connect, confirm that the Studio's
`VITE_OPENDUB_API_BASE` points to the same local API port and that the API process is running.
