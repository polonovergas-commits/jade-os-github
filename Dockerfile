# JADE OS V1.0 - Playwright-Ready Docker Image
# Base: Official Microsoft Playwright Python image (includes Chromium)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

LABEL maintainer="JADE OS Team"
LABEL version="1.0"
LABEL description="JADE OS - Market Intelligence & Content Automation Platform"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV USE_PAID_APIS=False
ENV ENVIRONMENT=production
ENV PORT=5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    redis-server \
    postgresql-client \
    gcc \
    libpq-dev \
    curl \
    wget \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    chromadb

RUN playwright install chromium --with-deps

COPY jade_os/ ./jade_os/
COPY workers/ ./workers/
COPY modules/ ./modules/
COPY dashboard.py .
COPY entrypoint.sh .
COPY scraping_config.json .

RUN mkdir -p /app/data/uploads \
    /app/data/processed \
    /app/data/memory \
    /app/data/temp_processing \
    /app/data/logs \
    /app/storage/normalized \
    /app/storage/temp \
    /app/logs

RUN chmod +x /app/entrypoint.sh

EXPOSE 5000
EXPOSE 8501
EXPOSE 6800

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["all"]
