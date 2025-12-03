#!/bin/bash
set -e

echo "=== JADE OS V1.0 Entrypoint ==="
echo "Mode: $1"

wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=1

    echo "Waiting for $service at $host:$port..."
    
    while [ $attempt -le $max_attempts ]; do
        if nc -z "$host" "$port" 2>/dev/null; then
            echo "$service is ready!"
            return 0
        fi
        echo "Attempt $attempt/$max_attempts: $service not ready, waiting..."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "ERROR: $service at $host:$port did not become ready in time"
    return 1
}

if [ -n "$DATABASE_URL" ]; then
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
        wait_for_service "$DB_HOST" "$DB_PORT" "PostgreSQL"
    fi
fi

if [ -n "$CELERY_BROKER_URL" ]; then
    REDIS_HOST=$(echo $CELERY_BROKER_URL | sed -n 's/.*\/\/\([^:]*\):.*/\1/p')
    REDIS_PORT=$(echo $CELERY_BROKER_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ -n "$REDIS_HOST" ] && [ -n "$REDIS_PORT" ]; then
        wait_for_service "$REDIS_HOST" "$REDIS_PORT" "Redis"
    fi
fi

echo "Initializing database..."
python -m jade_os.scripts.init_db 2>/dev/null || echo "Database init skipped or already initialized"

case "$1" in
    "api")
        echo "Starting FastAPI server on port 5000..."
        exec uvicorn jade_os.api.main:app --host 0.0.0.0 --port 5000
        ;;
    "dashboard")
        echo "Starting Streamlit dashboard on port 8501..."
        exec streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
        ;;
    "celery")
        echo "Starting Celery worker..."
        exec celery -A jade_os.workers.celery_app worker --loglevel=info --concurrency=2
        ;;
    "beat")
        echo "Starting Celery beat..."
        exec celery -A jade_os.workers.celery_app beat --loglevel=info
        ;;
    "all")
        echo "Starting ALL services (API + Dashboard + Redis)..."
        
        echo "Starting Redis server..."
        redis-server --port 6800 --daemonize yes
        sleep 2
        
        echo "Starting Celery worker in background..."
        celery -A jade_os.workers.celery_app worker --loglevel=info --concurrency=2 &
        CELERY_PID=$!
        sleep 2
        
        echo "Starting Celery beat in background..."
        celery -A jade_os.workers.celery_app beat --loglevel=info &
        BEAT_PID=$!
        sleep 2
        
        echo "Starting Streamlit dashboard in background..."
        streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true &
        STREAMLIT_PID=$!
        sleep 2
        
        echo "Starting FastAPI server (foreground)..."
        echo ""
        echo "=== JADE OS V1.0 READY ==="
        echo "API:       http://0.0.0.0:5000"
        echo "Dashboard: http://0.0.0.0:8501"
        echo "Redis:     localhost:6800"
        echo "==========================="
        echo ""
        
        exec uvicorn jade_os.api.main:app --host 0.0.0.0 --port 5000
        ;;
    *)
        echo "Starting custom command: $@"
        exec "$@"
        ;;
esac
