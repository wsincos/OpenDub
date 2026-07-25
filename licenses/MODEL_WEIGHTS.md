# Model Weights

OpenDub does not ship model weights in the repository or container images by default.

Each downloadable artifact must be added to `model-registry/upstreams.yaml` with a source URL, weight license or terms, file size, SHA-256, adapter compatibility version, and whether users must manually accept terms. An artifact with unknown terms or an unknown checksum remains unavailable to the automatic downloader.
