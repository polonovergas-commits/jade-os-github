# jade_os - Backend System

Backend-only project for jade_os system. No frontend, no UI - just APIs and background workers.

## Stack

- **Python 3.11+**
- **FastAPI** - HTTP API
- **PostgreSQL** - Main database
- **Redis** - Job queue
- **Celery** - Async workers
- **FFmpeg** - Video pipeline (skeleton)
- **Playwright** - Web scrapers (skeleton)
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation

## Project Structure

```
jade_os/
├── api/
│   ├── main.py              # FastAPI app with /healthz endpoint
│   └── routers/             # API route modules
├── core/
│   ├── config.py            # Settings and environment variables
│   ├── db.py                # PostgreSQL connection (SQLAlchemy)
│   ├── models.py            # Database models (jobs, videos, alerts)
│   ├── schemas.py           # Pydantic schemas for requests/responses
│   └── utils.py             # Utility functions
├── workers/
│   ├── celery_app.py        # Celery instance with Redis broker
│   ├── video_normalizer_worker.py      # Video normalization task (stub)
│   ├── story_aggregator_worker.py      # Story metadata aggregation (stub)
│   ├── domain_checker_worker.py        # Domain checking task (stub)
│   └── inventory_monitor_worker.py     # Inventory monitoring (stub)
└── scripts/
    ├── init_db.py           # Initialize database tables
    └── test_ffmpeg.py       # Test FFmpeg installation
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (copy .env.example to .env and update)

3. Initialize the database:
```bash
python -m jade_os.scripts.init_db
```

4. Test FFmpeg:
```bash
python -m jade_os.scripts.test_ffmpeg
```

## Running

### API Server
```bash
uvicorn jade_os.api.main:app --host 0.0.0.0 --port 5000 --reload
```

### Celery Workers
```bash
celery -A jade_os.workers.celery_app worker --loglevel=info
```

## API Endpoints

- `GET /` - Service info
- `GET /healthz` - Health check

## Database Models

- **Job** - Background job tracking
- **Video** - Video processing metadata
- **Alert** - System alerts and notifications

## Workers

All workers are currently stubs/skeletons ready for implementation:

- **normalize_video** - FFmpeg video normalization
- **aggregate_story_metadata** - Story metadata collection
- **check_domain** - Domain validation
- **monitor_inventory** - B2B inventory monitoring
