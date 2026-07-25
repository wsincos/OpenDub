# Contributing to OpenDub

OpenDub welcomes contributions to the platform, documentation, tests, examples, model adapters, and evaluation tools.

## Before You Start

1. Read [TODO/README.md](TODO/README.md) for the current architecture and delivery sequence.
2. Search existing issues before opening a new one.
3. Open an issue before substantial model, API, schema, or UI work so the scope can be agreed on.
4. Do not submit copyrighted video, unlicensed voice data, model weights with unclear terms, secrets, or personal data.

## Development Standards

- Write a failing test before production behavior changes.
- Keep core packages independent of PyTorch and model-specific dependencies.
- Preserve upstream copyright notices and add adapter provenance records.
- Update documentation and model cards for user-visible changes.
- Run the project checks listed in the relevant implementation task before opening a pull request.

## Pull Requests

Use a focused branch and a Conventional Commit title. Every pull request must explain:

- the user or developer behavior it changes;
- tests and validation commands run;
- license, model, data, or security implications;
- any migration or compatibility impact.

Model adapters begin as Experimental. They become Stable only after source, weight, license, contract-test, and real-inference verification.

## Code of Conduct

By participating, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
