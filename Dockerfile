# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy bot files
COPY bot ./bot
COPY scripts ./scripts
COPY pyproject.toml uv.lock* ./

# Create virtual environment
RUN pip install uv
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --upgrade pip

# Configure data volume
VOLUME ["/app/data"]
# Configure webhook port
EXPOSE 8443

# TODO: Healthcheck
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Run the bot
ENTRYPOINT ["uv", "run"]
