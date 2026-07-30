# Senscritique Cli

A minimal, modern starting point for Python services. Ships with structured
JSON logging (with optional Google Cloud Logging support), a `src/` layout, and
a fully wired tooling setup: [uv](https://docs.astral.sh/uv/) for dependency
management, [ruff](https://docs.astral.sh/ruff/) for linting and formatting,
[mypy](https://mypy.readthedocs.io/) for type checking, and `pytest` for tests.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.13 (uv will install it automatically if missing)

## Getting started

```bash
uv sync                  # create .venv and install all dependencies
cp .env.example .env     # configure environment variables
uv run python -m senscritique_cli
```

## Configuration

Configuration is read from environment variables (see `.env.example`):

| Variable            | Description                                                        | Default |
| ------------------- | ------------------------------------------------------------------ | ------- |
| `LOG_LEVEL`         | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL`                | `DEBUG` |
| `LOCAL_DEV`         | Truthy (`1`/`true`/`yes`) when running locally                    | `false` |
| `GOOGLE_PROJECT_ID` | When set, logs are emitted via Google Cloud's structured handler   | unset   |

## Development

Common tasks are exposed through the `Makefile`:

```bash
make install     # uv sync
make lint        # ruff check
make format      # ruff format
make typecheck   # mypy
make test        # pytest (unit)
make check       # lint + typecheck + test
make run         # run the app
```

```bash
make docker      # build the Docker image
```
```bash
make release version=0.2.0   # cut a release
```

Or call the tools directly via uv, e.g. `uv run pytest`.

### Pre-commit hooks

```bash
uv run pre-commit install
```

This runs ruff and a [gitleaks](https://github.com/gitleaks/gitleaks) secret
scan on every commit.

## Testing

Unit and integration tests live under `tests/`. Integration tests may require
external credentials (e.g. `GOOGLE_APPLICATION_CREDENTIALS`).

```bash
uv run pytest tests/unit          # fast, no external dependencies
uv run pytest tests/integration   # requires credentials
```

## Docker

```bash
docker build -t senscritique_cli:latest .
docker run --rm senscritique_cli:latest
```

The image uses a multi-stage `uv` build on `python:3.13-slim` and runs as a
non-root user.

## Releasing

```bash
make release version=0.2.0
```

This updates the version in `pyproject.toml`, refreshes `uv.lock`, commits,
tags, and pushes. The tag push triggers
[.github/workflows/release.yml](.github/workflows/release.yml), which builds
the package and publishes it to PyPI.

One-time setup on [pypi.org](https://pypi.org): under the project's
Publishing settings, add a trusted publisher with the repository owner,
repository name, workflow file `release.yml`, and environment `pypi`. No API
token is needed once that is configured.

## License

[MIT](./LICENSE)
