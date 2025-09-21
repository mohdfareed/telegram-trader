# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set work directory
WORKDIR /bot

# Copy app files
COPY app ./app
COPY scripts/app ./scripts/app
COPY scripts/setup.sh ./scripts/setup.sh
COPY pyproject.toml uv.lock* ./

# Configure container
VOLUME ["./data"]
ENV WEBHOOK_PORT=8443
EXPOSE 8443

# TODO: Healthcheck
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Set up environment
ENV PATH="/bot/scripts:$PATH"
RUN setup.sh

# Start the app
CMD ["app", "start"]
