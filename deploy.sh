#!/bin/bash
set -e

echo "=== JADE_OS Deploy Script ==="
echo ""

show_help() {
    echo "Usage: ./deploy.sh [command]"
    echo ""
    echo "Commands:"
    echo "  build       Build Docker images"
    echo "  up          Start all services (detached)"
    echo "  down        Stop all services"
    echo "  logs        Show logs (follow mode)"
    echo "  restart     Restart all services"
    echo "  status      Show service status"
    echo "  shell       Open shell in API container"
    echo "  test        Run API health check"
    echo ""
}

case "$1" in
    build)
        echo "Building Docker images..."
        docker-compose build --no-cache
        echo "Build complete!"
        ;;
    up)
        echo "Starting services..."
        docker-compose up -d
        echo ""
        echo "Services started! Checking health..."
        sleep 5
        docker-compose ps
        ;;
    down)
        echo "Stopping services..."
        docker-compose down
        echo "Services stopped."
        ;;
    logs)
        echo "Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    restart)
        echo "Restarting services..."
        docker-compose restart
        docker-compose ps
        ;;
    status)
        docker-compose ps
        echo ""
        echo "Health check:"
        curl -s http://localhost:8000/healthz | python3 -m json.tool 2>/dev/null || echo "API not responding"
        ;;
    shell)
        docker-compose exec api bash
        ;;
    test)
        echo "Testing API endpoints..."
        echo ""
        echo "1. Health check:"
        curl -s http://localhost:8000/healthz | python3 -m json.tool
        echo ""
        echo "2. OTTO SUPREME info:"
        curl -s http://localhost:8000/api/agent/otto/info | python3 -m json.tool
        echo ""
        echo "3. Arsenal list:"
        curl -s http://localhost:8000/api/agent/arsenal/list | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Total strategies: {len(d[\"strategies\"])}')"
        echo ""
        echo "All tests passed!"
        ;;
    *)
        show_help
        ;;
esac
