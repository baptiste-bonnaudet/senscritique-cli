# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:0.12 AS uv

# ---- builder ----------------------------------------------------------------
FROM python:3.14-slim AS builder

COPY --from=uv /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Install dependencies first (cached) using only the lockfile and manifest.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --locked --no-install-project --no-dev

# Install the project itself.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ---- runtime ----------------------------------------------------------------
FROM python:3.14-slim AS runtime

LABEL maintainer="baptiste.bonnaudet@gmail.com"

RUN useradd --create-home --uid 1001 app

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
USER app

CMD ["python", "-m", "senscritique_cli"]
