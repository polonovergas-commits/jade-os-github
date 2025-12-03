# JADE_OS - Blueprint Completo

## Visao Geral

Sistema backend de inteligencia viral para processamento de midia, captura de sinais sociais e monitoramento de infraestrutura.

**Stack**: Python 3.11 | FastAPI | PostgreSQL | Redis | Celery | FFmpeg

---

## Arquitetura

```
jade_os/
├── api/
│   ├── main.py              # FastAPI app principal
│   └── routers/
│       ├── jobs.py          # CRUD de jobs
│       ├── ingest.py        # Ingestao de midia
│       ├── intelligence.py  # Operacoes de inteligencia
│       └── metrics.py       # Metricas do sistema
├── core/
│   ├── config.py            # Configuracoes
│   ├── db.py                # Conexao PostgreSQL
│   ├── models.py            # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas
├── workers/
│   ├── celery_app.py        # Celery config
│   ├── video_normalizer_worker.py
│   ├── social_signal_worker.py
│   ├── infrastructure_probe_worker.py
│   └── supply_chain_worker.py
└── scripts/
    └── init_db.py           # Inicializacao do banco

modules/
└── auron_brain/             # Motor de IA
    ├── engine.py            # AuronEngine principal
    ├── commands.py          # Comandos
    ├── context.py           # Gerenciamento de contexto
    ├── prompts.py           # Templates de prompts
    ├── signatures.py        # Assinaturas
    └── strategies.py        # Estrategias de resposta

workers/
└── ghost_processor.py       # Processador FFmpeg (camuflagem)
```

---

## API Endpoints

### Health & Info
| Method | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/` | Info do servico |
| GET | `/healthz` | Health check |

### Jobs
| Method | Endpoint | Descricao |
|--------|----------|-----------|
| POST | `/jobs/` | Criar job |
| GET | `/jobs/` | Listar jobs (filtros: type, status, module) |
| GET | `/jobs/{job_id}` | Buscar job por UUID |

### Ingestao
| Method | Endpoint | Descricao |
|--------|----------|-----------|
| POST | `/ingest/media` | Ingerir midia para normalizacao |

### Inteligencia
| Method | Endpoint | Descricao |
|--------|----------|-----------|
| POST | `/intel/social/scan` | Capturar sinais sociais |
| POST | `/intel/infra/check` | Verificar disponibilidade de infraestrutura |
| POST | `/intel/supply/track` | Monitorar cadeia de suprimentos |

### Metricas
| Method | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/metrics/system` | Metricas agregadas (jobs por status/tipo) |

---

## Modelos de Dados

### Job
```python
id: UUID
type: str           # NORMALIZE_MEDIA, SOCIAL_SCAN, INFRA_CHECK, SUPPLY_TRACK
module: str         # video_normalizer, social_signal, etc.
status: str         # PENDING, RUNNING, COMPLETED, FAILED
priority: int       # 1-10
payload: JSON
result: JSON
error_message: str
retry_count: int
created_at: datetime
updated_at: datetime
```

### VideoAsset
```python
id: UUID
source_url: str
normalized_url: str
original_hash: str      # SHA256
normalized_hash: str    # SHA256
duration: float
size_bytes: int
status: str             # PENDING, PROCESSING, COMPLETED, FAILED
created_at: datetime
```

### SignalCapture
```python
id: UUID
source_type: str        # SOCIAL_STORY, SOCIAL_POST, etc.
target_identifier: str  # @username, hashtag, etc.
external_id: str
payload_json: JSONB
captured_at: datetime
created_at: datetime
```

### MarketProbe
```python
id: UUID
target_url: str
http_status_code: int
latency_ms: float
is_available: bool
checked_at: datetime
created_at: datetime
```

### SupplyChainSnapshot
```python
id: UUID
sku: str
supplier_id: str
stock_level: int
price_point: float
snapshot_at: datetime
created_at: datetime
```

---

## Workers (Celery Tasks)

### 1. Video Normalizer
**Task**: `normalize_media_asset`
- Download do video fonte
- Hash SHA256 original
- FFmpeg hardening:
  - `-map_metadata -1` (remove metadata)
  - `eq=gamma=1.01` (ajuste sutil)
  - `loudnorm` (normalizacao de audio)
  - CBR audio 192k
- Hash SHA256 normalizado
- Persistencia em `storage/normalized/`

### 2. Ghost Processor (Camuflagem)
**Funcao**: `process_video_upload`
- Perfis de dispositivo iPhone (15 Pro Max, 15 Pro, 14 Pro Max, 13 Pro)
- Gamma aleatorio (0.99-1.01)
- Metadados Apple injetados
- Output: `IMG_XXXX.MOV`

### 3. Social Signal Worker
**Task**: `capture_social_signal`
- Captura de dados sociais
- Armazena em SignalCapture

### 4. Infrastructure Probe Worker
**Task**: `probe_infrastructure`
- HTTP HEAD request
- Medicao de latencia
- Status de disponibilidade

### 5. Supply Chain Worker
**Task**: `track_supply_chain`
- Monitoramento de estoque
- Rastreamento de precos

---

## Auron Brain (Motor IA)

### Componentes
| Arquivo | Funcao |
|---------|--------|
| `engine.py` | AuronEngine - motor principal OpenAI |
| `commands.py` | Processamento de comandos |
| `context.py` | Gerenciamento de contexto de conversacao |
| `prompts.py` | Templates de prompts (50KB+) |
| `signatures.py` | Assinaturas de funcoes |
| `strategies.py` | Estrategias de resposta |

---

## Docker

### Servicos
| Servico | Imagem | Porta |
|---------|--------|-------|
| api | python:3.11-slim | 8000 |
| worker | python:3.11-slim | - |
| db | postgres:15-alpine | 5432 |
| redis | redis:7-alpine | 6379 |

### Volumes
- `postgres_data` - Dados PostgreSQL
- `redis_data` - Dados Redis
- `media_storage` - Midias normalizadas

### Deploy
```bash
cp .env.example .env
docker-compose up -d --build
```

---

## Variaveis de Ambiente

```env
# Database
DATABASE_URL=postgresql://jade:password@db:5432/jade_os
POSTGRES_USER=jade
POSTGRES_PASSWORD=jade_secret
POSTGRES_DB=jade_os

# Redis/Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000

# Storage
STORAGE_DIR=/app/storage
```

---

## Exemplos de Uso

### Ingerir Midia
```bash
curl -X POST http://localhost:8000/ingest/media \
  -H "Content-Type: application/json" \
  -d '{"source_url": "https://example.com/video.mp4"}'
```

### Scan Social
```bash
curl -X POST http://localhost:8000/intel/social/scan \
  -H "Content-Type: application/json" \
  -d '{"source_type": "SOCIAL_STORY", "target_identifier": "@username"}'
```

### Check Infraestrutura
```bash
curl -X POST http://localhost:8000/intel/infra/check \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://target-domain.com"}'
```

### Track Supply Chain
```bash
curl -X POST http://localhost:8000/intel/supply/track \
  -H "Content-Type: application/json" \
  -d '{"sku": "PROD-001", "supplier_id": "SUPPLIER-A"}'
```

### Metricas
```bash
curl http://localhost:8000/metrics/system
```

---

## Repositorio

**GitHub**: https://github.com/polonovergas-commits/jade-x-viral-intelligence

## Status: PRODUCTION READY
