# Local Alpha Quick Start

This guide runs the currently implemented, local-only OpenDub alpha. It creates a project,
imports local media, records a voice-rights declaration, and adds a timeline segment. It does
not install or claim a real dubbing model.

## Prerequisites

- Linux or macOS with Python 3.11 through 3.13;
- FFmpeg and FFprobe on `PATH`;
- Node.js 20+ for the Web Studio;
- `uv` for Python dependencies and `pnpm` for the Web workspace.

## Install and verify

```bash
git clone https://github.com/GalaxyCong/OpenDub.git
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

## Alpha workflow

1. Create a local project in the Studio.
2. Import a video, a subtitle file, or an audio file that you own or are authorized to use.
3. For an audio file used as a voice reference, record the material source and a speaker label.
4. Add dialogue with a target start/end time, language, voice reference, emotion direction, and intensity.
5. Review the stored project revision and the resulting timeline segment.

The Studio will state that no model is verified until an adapter has passed the model admission
gate. Do not interpret the `planned` status in the model registry as an available generation backend.

## Command line basics

```bash
uv run opendub create "Authorized demo" --workspace ~/.local/share/opendub
uv run opendub list --workspace ~/.local/share/opendub
uv run opendub doctor --workspace ~/.local/share/opendub --json
```

## Troubleshooting

`opendub doctor` reports missing FFmpeg, an unwritable workspace, or registry issues without
reading user media into telemetry. If the browser cannot connect, confirm that the Studio's
`VITE_OPENDUB_API_BASE` points to the same local API port and that the API process is running.

