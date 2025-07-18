FROM python:3.10-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /usr/local/bin/uv

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev portaudio19-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN uv venv

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    .venv/bin/python -m uv pip install --no-cache-dir -r requirements.txt


FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg vlc libportaudio2 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["python", "run.py"]
