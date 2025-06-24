# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13
ARG NODE_VERSION=22.15.0
ARG PNPM_VERSION=10.12.1

################################################################################
FROM node:${NODE_VERSION}-alpine AS static

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
  npm install -g pnpm@${PNPM_VERSION}

RUN --mount=type=bind,source=package.json,target=package.json \
  --mount=type=bind,source=pnpm-lock.yaml,target=pnpm-lock.yaml \
  --mount=type=cache,target=/root/.local/share/pnpm/store \
  pnpm install --frozen-lockfile

COPY . .

RUN pnpm run build

################################################################################
FROM python:${PYTHON_VERSION}-slim

ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

WORKDIR /app

ARG UID=10001
RUN adduser \
  --disabled-password \
  --gecos "" \
  --home "/nonexistent" \
  --shell "/sbin/nologin" \
  --no-create-home \
  --uid "${UID}" \
  appuser

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-editable --no-dev

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

COPY . .

EXPOSE 8000

COPY --from=static /app/dist ./dist

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]