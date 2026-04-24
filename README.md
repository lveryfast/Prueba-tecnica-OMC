# Lead Management API

API REST para gestión de leads con análisis de IA integrado.

## Stack Tecnológico

| Tecnología | Decisión |
|------------|----------|
| **FastAPI** | Rendimiento async, validación automática con Pydantic, Swagger incluido |
| **PostgreSQL** | Robustez transactional, soporte JSON, Índices powerful |
| **SQLAlchemy 2.0** | ORM con soporte async nativo, type-safe queries |
| **JWT (python-jose)** | Tokens stateless, escalable horizontalmente |
| **Docker** | Reproducibilidad, environment consistente |
| **Alembic** | Migraciones versionadas, rollback seguro |

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ��─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Routes        │  │   Middleware    │  │  Handlers   │ │
│  │   (Controllers) │  │   (Auth, CORS)   │  │  (Errors)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    APPLICATION LAYER                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Use Cases     │  │     DTOs        │  │   Ports      │ │
│  │   (Business)    │  │  (Validation)   │  │ (Interfaces) │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                      DOMAIN LAYER                            │
│  ┌─────────────────┐  ┌─────────────────┐                    │
│  │   Entities      │  │  Interfaces     │                    │
│  │   (Lead, User)  │  │  (Contracts)     │                    │
│  └─────────────────┘  └─────────────────┘                    │
├─────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE LAYER                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐│
│  │   Database      │  │  Repositories   │  │  Services    ││
│  │   (SQLAlchemy)   │  │   (Impl)        │  │ (Auth, AI)   ││
│  └─────────────────┘  └─────────────────┘  └─────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Principios aplicados:**
- **Dependency Inversion**: Capas externas dependen de abstracciones en domain
- **Single Responsibility**: Cada clase tiene una razón para cambiar
- **Open/Closed**: Extensible sin modificar código existente

## Instalación

### Local (Python 3.11+)

```bash
git clone https://github.com/lveryfast/Prueba-tecnica-OMC.git
cd Prueba-tecnica-OMC

python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt

# Crear DB PostgreSQL
psql -U postgres -c "CREATE DATABASE leads_db;"

# Copiar y configurar .env
copy .env.example .env

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

### Docker

```bash
docker-compose up --build
```

## API Endpoints

### Autenticación

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@leads.com","password":"admin123"}'
```

### Leads (CRUD)

```bash
# Crear lead
curl -X POST http://localhost:8000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Pérez","email":"juan@email.com","telefono":"+573012345678","fuente":"instagram","producto_interes":"Curso","presupuesto":299.99}'

# Listar con filtros y paginación
curl "http://localhost:8000/api/leads?page=1&limit=10&fuente=instagram"

# Filtrar por fecha
curl "http://localhost:8000/api/leads?start_date=2024-01-01&end_date=2024-12-31"

# Obtener lead por ID
curl http://localhost:8000/api/leads/{id}

# Actualizar lead
curl -X PATCH http://localhost:8000/api/leads/{id} \
  -H "Content-Type: application/json" \
  -d '{"presupuesto":350.00}'

# Eliminar lead (soft delete)
curl -X DELETE http://localhost:8000/api/leads/{id}

# Estadísticas
curl http://localhost:8000/api/leads/stats
```

### IA (Mock)

```bash
curl -X POST http://localhost:8000/api/leads/ai/summary
curl -X POST "http://localhost:8000/api/leads/ai/summary?fuente=instagram"
```

### Webhook

```bash
curl -X POST http://localhost:8000/api/leads/webhook \
  -H "Content-Type: application/json" \
  -d '{"nombre":"External Lead","email":"external@email.com","fuente":"facebook"}'
```

## Documentación API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Tests

```bash
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest --cov=app tests/ --cov-report=html
```

## Decisiones Técnicas

### ¿Por qué async?
PostgreSQL con asyncpg permite manejar miles de conexiones concurrentes sin blocking I/O.

### ¿Por qué Alembic?
Migraciones versionadas permiten rollback seguro y deployment reproducible.

### ¿Por qué Strategy Pattern en IA?
Permite cambiar de mock a OpenAI sin modificar código de negocio.

### ¿Por qué soft delete?
Preserva integridad referencial y permite auditoría histórica.

## Usuarios de Prueba

| Email | Password | Rol |
|-------|----------|-----|
| admin@leads.com | admin123 | admin |

## License

MIT