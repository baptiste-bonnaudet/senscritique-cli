# CLAUDE.md

Project context for coding agents working in this repository.

## Stack

- Python 3.13, managed with [uv](https://docs.astral.sh/uv/).
- `src/` layout: package code lives in `src/senscritique_cli`, unit tests in
  `tests/unit`.
- Linting and formatting with [ruff](https://docs.astral.sh/ruff/), strict
  type checking with `mypy`.

## Make targets

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
make release version=0.2.0   # bump version, tag, push
```

Run `make check` before committing.

## Releasing

`make release version=X.Y.Z` bumps `pyproject.toml`, refreshes `uv.lock`,
commits, tags, and pushes. The tag push runs
`.github/workflows/release.yml`, which builds the package and publishes it to
PyPI via trusted publishing.
