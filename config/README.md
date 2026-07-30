# Project Configuration

Machine-readable project contracts live here rather than at the repository
root. They are versioned alongside the code that consumes them.

- `model-registry/` records the source, revision, license, and admission state
  of each upstream research method.
- `schemas/` contains the public JSON Schema contracts emitted by
  `python scripts/export_schemas.py`.

Use `python scripts/verify_registry.py` to validate the model registry.
