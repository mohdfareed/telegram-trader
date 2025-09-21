# syntax=docker/dockerfile:1

# Use python with uv
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy app files
WORKDIR /bot
COPY app ./app
COPY scripts/app ./scripts/app
COPY scripts/setup.sh ./scripts/setup.sh
COPY pyproject.toml uv.lock* ./

# Configure container
VOLUME ["./data"]
EXPOSE ${WEBHOOK_PORT}
ENV PATH="/bot/scripts:$PATH"
RUN setup.sh

# Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD app health || exit 1

# Start the app
CMD ["app", "start"]
