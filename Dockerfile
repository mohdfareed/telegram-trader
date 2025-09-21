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

# TODO: Healthcheck
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Start the app
CMD ["app", "start"]
