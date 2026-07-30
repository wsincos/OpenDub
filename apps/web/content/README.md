# Web Content Catalog

This directory contains the declarative content rendered by the OpenDub web
application. It is intentionally separate from `src/`, which contains React
components and application behavior.

- `methods/` defines the team's complete method records and their interactive
  component descriptions.
- `showcases/` defines the authorization-aware manifests for public archived
  media examples.
- `cases/` retains short, non-runtime concept records used by the interface.

The web application imports these JSON documents directly; update the related
tests whenever a public record changes.
