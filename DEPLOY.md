# JADE_OS Production Deployment Guide

## Quick Start

### Option 1: VPS with Docker Compose

```bash
# 1. Clone repository
git clone <your-repo-url>
cd jade_os

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with your production values

# 3. Build and start
./deploy.sh build
./deploy.sh up

# 4. Verify deployment
./deploy.sh test
```

### Option 2: Railway

1. Connect your GitHub repository to Railway
2. Railway will auto-detect the `railway.toml` configuration
3. Add environment variables in Railway dashboard:
   - `DATABASE_URL` (Railway provides PostgreSQL)
   - `REDIS_URL` (Railway provides Redis)
   - `USE_PAID_APIS=false`

4. Deploy!

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      JADE_OS v1.1.0                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │   API   │    │ Worker  │    │  Beat   │    │  Redis  │  │
│  │ :8000   │◄───│ Celery  │◄───│ Celery  │◄───│  :6379  │  │
│  └────┬────┘    └────┬────┘    └─────────┘    └─────────┘  │
│       │              │                                      │
│       └──────────────┼──────────────────────────────────┐  │
│                      │                                   │  │
│                      ▼                                   │  │
│               ┌─────────────┐                            │  │
│               │  PostgreSQL │                            │  │
│               │    :5432    │                            │  │
│               └─────────────┘                            │  │
│                                                          │  │
└──────────────────────────────────────────────────────────┘
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| API | 8000 | FastAPI application (44+ endpoints) |
| Worker | - | Celery background workers |
| Beat | - | Celery scheduler (optional) |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Cache + Celery broker |

---

## Endpoints Overview

### OTTO SUPREME (AI Strategy)
- `POST /api/agent/otto/chat` - Full cognitive pipeline
- `GET /api/agent/otto/info` - System info (48 nuclei, 18 specialists)
- `POST /api/agent/leon/diagnostic` - Deep analysis
- `POST /api/agent/reasoner/analyze` - ROI + Monte Carlo
- `GET /api/agent/arsenal/list` - 50+ strategies

### Shopee Intelligence
- `POST /api/shopee/hunt` - Product hunting
- `POST /api/shopee/analyze` - Market analysis
- `GET /api/shopee/regions` - 7 supported regions

### Content Factory
- `POST /api/factory/process` - Video processing
- `POST /api/factory/wash` - Video washing
- `POST /api/factory/ghost` - Ghost processor

### Jobs & Operations
- `POST /jobs/dispatch` - Dispatch Celery tasks
- `GET /jobs/{job_id}` - Get job status
- `GET /ops/warroom/status` - System status

---

## Environment Variables

### Required
```env
DATABASE_URL=postgresql://user:pass@host:5432/jade_os
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
```

### Optional (for AI features)
```env
USE_PAID_APIS=true
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=...
ELEVENLABS_API_KEY=...
```

---

## Commands

```bash
# Build
./deploy.sh build

# Start/Stop
./deploy.sh up
./deploy.sh down

# Monitor
./deploy.sh logs
./deploy.sh status

# Test
./deploy.sh test

# Shell access
./deploy.sh shell
```

---

## Health Checks

```bash
# API health
curl http://localhost:8000/healthz

# OTTO SUPREME
curl http://localhost:8000/api/agent/otto/info

# Full test suite
./deploy.sh test
```

---

## Scaling

### Workers
```bash
# Increase worker concurrency
docker-compose exec worker celery -A jade_os.workers.celery_app worker --concurrency=8
```

### Multiple Workers
```yaml
# Add to docker-compose.yml
worker-2:
  <<: *worker
  container_name: jade_os_worker_2
```

---

## Troubleshooting

### Playwright/Chromium Issues
```bash
# Inside container
docker-compose exec api playwright install chromium --with-deps
```

### Database Migrations
```bash
docker-compose exec api python -m jade_os.scripts.init_db
```

### Redis Connection
```bash
docker-compose exec redis redis-cli ping
# Should return: PONG
```

---

## Production Checklist

- [ ] Strong passwords in `.env`
- [ ] `USE_PAID_APIS=false` (or configure API keys)
- [ ] Firewall rules (only expose port 8000)
- [ ] SSL/TLS via reverse proxy (nginx/caddy)
- [ ] Backup strategy for PostgreSQL
- [ ] Monitoring (logs, metrics)

---

## Support

JADE_OS v1.1.0 - OTTO SUPREME AURON-NATIVE
