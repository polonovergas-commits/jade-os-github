# jade_os Project - Backend System

## Overview
`jade_os` is a backend-only system for advanced market intelligence, content generation, and data processing. It provides deep insights into e-commerce markets, generates diverse content, and processes media with anti-detection and stealth protocols. The project's vision is to be the leading intelligence and content automation platform for e-commerce, enabling market opportunity identification, competitor tracking, and rapid content production.

**Key Capabilities**:
- Multi-region e-commerce product scraping with velocity scoring.
- Advanced web scraping with anti-detection and human-like behavior simulation.
- AI-powered market intelligence and content script generation (AURON Brain).
- Robust video processing (FFmpeg) for content manipulation and obfuscation (Ghost Processor, Content Factory).
- Universal data ingestion and a vector-based memory store (Supermemory).
- Comprehensive job management and system observability.

## User Preferences
- Focus on backend-only solutions.
- No frontend/UI development.
- Clean, organized code structure.
- USE_PAID_APIS = False (scrapers + local FFmpeg only).
- Ready for deployment to Railway + VPS.

## System Architecture

**Core Components**:
- **API Layer**: FastAPI application serving as the central interface.
- **AURON Brain**: AI-driven intelligence module for market analysis, strategy generation, and content ideation.
- **Ghost Processor**: Utilizes FFmpeg for advanced video camouflage and anti-detection.
- **Shopee Nuclear**: Multi-region product intelligence worker for Shopee data scraping.
- **Content Factory**: FFmpeg-based video processing pipeline, including AI-driven script generation and voice synthesis.
- **Supermemory**: Vector-based memory store for intelligent data recall and query.
- **Social Scraper**: Web scraping with Playwright Stealth for social signal intelligence.
- **Proxy Management System**: Centralized system with Redis for proxy storage, rotation, and anti-bot handling.
- **Auron Brain Module**: AI-powered intelligence with centralized prompts and anti-bot resolution.
- **Task Feedback System**: API for monitoring and managing Celery task statuses.
- **Chat Context Manager**: Redis-based system for persisting chat history.
- **Scraping Cache Manager**: Caches scraping results in Redis to prevent redundant operations.
- **OTTO SUPREME AURON-NATIVE**: Strategic AI agent with cognitive architecture, internal debate specialists, and diverse strategic modules.
- **Task Scheduler**: Redis-based scheduling system for periodic scraping tasks (interval and cron).
- **Notifier**: Alert system with Telegram support for critical failure notifications.
- **Celery Beat**: Periodic task scheduler for automated scraping jobs.

**Technical Implementations and Design Choices**:
- **Data Persistence**: PostgreSQL with SQLAlchemy ORM.
- **Caching & Job Queue**: Redis for deduplication, caching, and Celery job queue.
- **Asynchronous Processing**: Celery for background tasks.
- **Web Scraping**: Playwright with advanced stealth techniques (e.g., Canvas, WebGL, Audio fingerprint spoofing, human behavior simulation).
- **Video Processing**: FFmpeg for all video manipulation.
- **Modularity**: Clearly defined FastAPI routers for functionalities.
- **Scalability**: Designed for Railway/VPS deployment with distributed workers.
- **Evasion Techniques**: Extensive anti-detection layers and randomization for stealthy operations.
- **Proxy Management**: Redis-based proxy storage, automatic rotation, and anti-bot handling (CAPTCHA detection, auto-reload).
- **AI Integration**: AURON Brain for anti-bot resolution and content generation, with fallback for disabled paid APIs.
- **Chat Context**: Redis for chat history persistence with auto-expiry.
- **Scraping Cache**: Redis for caching scraping results by keyword/page/region.
- **Task Scheduling**: TaskScheduler module with Redis persistence for interval/cron scheduling.
- **Notification System**: Notifier module with Telegram Bot API integration for alerts.
- **Celery Beat Integration**: Persistent scheduler for periodic task execution.

## Recent Changes (Block 12 - December 2025)

### JADE OS V1.0 - Cockpit & Launch Complete:
- **Streamlit Dashboard**: Command Center com 4 tabs operacionais (porta 8080)
  - Tab 1: Shopee Nuclear Radar (multi-country scan)
  - Tab 2: Ghost Protocol (video upload/processing)
  - Tab 3: Strategy Brain (OTTO chat com memória)
  - Tab 4: System Status (health checks)
- **VectorMemory**: Memória de longo prazo (ChromaDB/Redis/JSON fallback)
- **Dockerfile Playwright-Ready**: Base mcr.microsoft.com/playwright/python:v1.40.0-jammy
- **entrypoint.sh Multi-Mode**: api/dashboard/celery/beat/all
- **Test Suite Completo**: 60 testes, 100% sucesso
  - VectorMemory: 8/8
  - AuronEngine: 2/2
  - AuronEngineV2: 2/2
  - StrategyRouter: 3/3
  - GhostProcessor: 6/6
  - SupplyChainV3: 6/6
  - SocialSignalWorker: 11/11
  - Celery Tasks: 5/5
  - Notifier: 2/2
  - TaskScheduler: 2/2
  - Redis: 4/4
  - PostgreSQL: 3/3
  - API: 4/4
  - Streamlit: 2/2

### Files Added:
- `dashboard.py` - Streamlit Command Center
- `jade_os/modules/auron_brain/memory.py` - VectorMemory
- `tests/test_all_modules.py` - Comprehensive Test Suite
- `data/test_results.json` - Test Results

## Recent Changes (Block 11 - December 2025)

### SupplyChainWorkerV3 - Playwright Shopee Scraper:
- **Migração para Playwright**: Removido cloudscraper/httpx/BeautifulSoup, agora usa Playwright para execução de JavaScript
- **Foco Shopee**: Exclusivamente focado na Shopee, removida lógica para Amazon e MercadoLivre
- **Interceptação de API**: Captura respostas JSON das APIs internas da Shopee para dados reais de estoque e preço
- **Fallback DOM**: Extração via regex do DOM renderizado quando API não disponível
- **ProxyManagerV3**: Integração com proxies residenciais via variáveis PROXY_HOST/PORT/USER/PASS
- **Teste de Proxy**: Validação de proxy via httpbin.org antes de cada operação
- **Anti-Detecção Playwright**: webdriver=undefined, plugins fake, languages fake, geolocation Brasil
- **CircuitBreakerV3**: Auto-disable domínios falhos (5 failures = 5min timeout)
- **RateLimiterV3**: Delay randomizado 3-7s entre requisições por domínio
- **7 Regiões Shopee**: BR, SG, MY, TH, VN, PH, ID com moedas e domínios específicos

### Files Added/Updated:
- `jade_os/workers/supply_chain_worker_v3.py` - Novo worker com Playwright
- `jade_os/api/routers/intelligence.py` - Atualizado para usar V3
- `jade_os/workers/celery_app.py` - Rota adicionada para task V3

## Previous Changes (Block 10 - December 2025)

### AuronEngineV2 - Optimized AI Engine:
- **SemanticCache**: Intelligent caching with semantic similarity matching (30-40% cache hit rate)
- **CircuitBreaker**: Auto-disable failing APIs (5 failures = 60s timeout) with HALF_OPEN recovery
- **RateLimiter**: Per-provider request limiting (60 req/min default)
- **ContextManagerV2**: Thread-safe context with async locks (FIX race conditions)
- **Input Sanitization**: HTML/script tag removal, length limiting (FIX injection vulnerability)
- **Timeout Handling**: 30s API timeout with fallback responses
- **Memory Management**: Context compression at 8000 tokens, conversation TTL (24h default)
- **Backwards Compatibility**: V1 API preserved, get_optimized_engine() for V2 access

### Files Added/Updated:
- `jade_os/modules/auron_brain/engine_v2.py` - New V2 engine with all optimizations
- `jade_os/modules/auron_brain/engine.py` - Updated with V2 imports and compatibility layer

### Bug Fixes in AuronEngineV2:
1. Race condition in context manager (async locks)
2. Memory leak in HTTP connections (proper cleanup)
3. JSON decode error without fallback (safe parsing)
4. No timeout in API calls (30s limit)
5. No rate limiting (60 req/min)
6. No circuit breaker (5 failures threshold)
7. No cache (semantic cache with TTL)
8. Context grows indefinitely (compression at 8k tokens)
9. No input validation (sanitization added)

### API main.py V2 - Security Hardening:
- **CORS Middleware**: Configured via ALLOWED_ORIGINS env var
- **Rate Limiting**: 100 req/min via SlowAPI
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy, Cache-Control
- **HSTS**: Enabled in production mode only
- **Error Handling**: Global exception handlers sanitize errors in production
- **Request Tracing**: X-Request-ID header on all responses
- **GZip Compression**: Enabled for responses > 1000 bytes
- **Health Checks**: Database, Redis, Celery status verification
- **Prometheus Metrics**: /metrics endpoint for monitoring

### New Dependencies:
- slowapi (rate limiting)
- psutil (system info)
- prometheus-client (metrics)

## Previous Changes (Block 9 - December 2025)

### GhostProcessorV2 - Enhanced Video Camouflage:
- SecuritySanitizer: Command injection prevention
- VideoValidator: Input/output validation with ffprobe
- Retry Logic: 3 attempts with exponential backoff
- Timeout: 5-8 minutes per attempt
- Device Profiles: iPhone 13/14/15 Pro with realistic metadata
- Unique job directories: Fixes race conditions
- Structured logging: JSON with hash, timing, size metrics

### SupplyChainWorkerV2 - Real Scraping with Anti-Detection:
- ProxyManager: Intelligent proxy rotation with success rate tracking
- RateLimiter: Domain-based delay system
- CircuitBreaker: Auto-disable failing domains (5 failures = 5min timeout)
- SecurityConfig: 8+ User-Agents with site-specific headers
- CloudScraper: Cloudflare bypass integration
- Scrapers: Amazon, AliExpress, MercadoLivre with BeautifulSoup parsing
- Removed: Mock/simulated data (replaced with real scraping)

### Files Updated:
- `workers/ghost_processor.py` - Full rewrite with V2 architecture
- `jade_os/workers/supply_chain_worker.py` - Full rewrite with anti-detection
- `jade_os/workers/social_signal_worker.py` - Fixed playwright_stealth import
- `scraping_config.json` - New configuration file for scrapers

### Previous Changes (Block 8):
- Task Scheduler: Interval and CRON scheduling via Celery Beat
- Notifier: Telegram alerts for critical failures
- Scheduling endpoints for periodic scraping tasks

## External Dependencies

- **Python 3.11**
- **FastAPI + Uvicorn**
- **PostgreSQL**
- **Redis**
- **Celery**
- **FFmpeg**
- **Playwright**
- **aiohttp + aioredis**
- **Brotli/Gzip**
- **Telegram** (for notifications)