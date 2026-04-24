# Lead Management API

API REST para gestión de leads con análisis de IA integrado.

## Stack Tecnológico

| Tecnología | Decisión | Por qué |
|------------|----------|--------|
| **FastAPI** | Framework | Rendimiento async nativo, validación automática con Pydantic, Swagger/OpenAPI incluido |
| **PostgreSQL** | Base de datos | Robustez transactional, soporte JSON, índices compostos poderosos, estándar industrial |
| **SQLAlchemy 2.0** | ORM | Soporte async nativo (asyncpg), type-safe queries, abstracción de DB |
| **JWT (python-jose)** | Autenticación | Tokens stateless, escalable horizontalmente, estándar RFC 7519 |
| **Docker** | Container | Reproducibilidad, environment consistente, no "en mi máquina funciona" |
| **Alembic** | Migraciones | Migraciones versionadas, rollback seguro, deployment reproducible |
| **SlowAPI** | Rate limiting | Protección contra abuse, límites configurables por endpoint |

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Routes        │  │   Middleware    │  │  Handlers   │ │
│  │   (Endpoints)  │  │   (Auth, CORS)  │  │  (Errors)    │ │
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
│  │   (Lead, User) │  │  (Contracts)     │                    │
│  └─────────────────┘  └─────────────────┘                    │
├─────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE LAYER                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐│
│  │   Database      │  │  Repositories   │  │  Services    ││
│  │   (SQLAlchemy)   │  │   (Impl)        │  │ (Auth, AI)   ││
│  └────────────���────┘  └─────────────────┘  └─────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Principios aplicados:**
- **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Clean Architecture**: Capas independientes, dependencias apuntan hacia adentro
- **Soft Delete**: Preserva integridad referencial y auditoría histórica
- **Strategy Pattern**: AI service puede cambiarse de mock a real sin modificar código

## Error Handling

Todos los endpoints manejan errores de forma consistente:

```json
{
  "success": false,
  "error": {
    "type": "validation_error",
    "detail": "..."
  },
  "message": "Mensaje legible para el usuario",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Códigos de error:**
- `400` - Error de validación / datos inválidos
- `401` - No autenticado
- `403` - No autorizado
- `404` - Recurso no encontrado
- `409` - Conflicto (email duplicado)
- `422` - Error de validación de Pydantic
- `429` - Rate limit excedido
- `500` - Error interno del servidor

## Instalación

### Prerrequisitos

- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)

### Configuración Local

```bash
# 1. Clonar repositorio
git clone https://github.com/lveryfast/Prueba-tecnica-OMC.git
cd Prueba-tecnica-OMC

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear base de datos PostgreSQL
psql -U postgres -c "CREATE DATABASE leads_db;"

# 5. Copiar configuración
copy .env.example .env

# 6. Editar .env con tus valores
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/leads_db
# JWT_SECRET_KEY=tu-secret-key-min-32-caracteres
```

### Ejecutar Migraciones

```bash
# Aplicar migraciones
alembic upgrade head
```

### Seed - Crear Usuario Admin

```bash
# El usuario admin se crea automáticamente al iniciar la app
# o puedes ejecutar el SQL directamente:

psql -U postgres -d leads_db -f insert_admin.sql
```

**Credenciales por defecto:**
- Email: `admin@leads.com`
- Password: `admin123`

### Iniciar Servidor

```bash
# Desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O con Docker
docker-compose up --build
```

## API Endpoints

### Autenticación

```bash
# Login - Obtener token JWT
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@leads.com","password":"admin123"}'

# Respuesta:
# {
#   "access_token": "eyJ...",
#   "expires_in": 1800,
#   "user": {"email": "admin@leads.com", "nombre": "Admin", "rol": "admin"}
# }
```

### Leads CRUD

```bash
# Headers requeridos para endpoints protegidos
TOKEN="tu-jwt-token"

# Crear lead
curl -X POST http://localhost:8000/api/leads \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Pérez","email":"juan@email.com","telefono":"+573012345678","fuente":"instagram","producto_interes":"Curso","presupuesto":299.99}'

# Listar leads (con paginación, filtros, sorting)
curl "http://localhost:8000/api/leads?page=1&limit=10&fuente=instagram&sort_by=created_at&sort_order=desc" \
  -H "Authorization: Bearer $TOKEN"

# Filtros adicionales
curl "http://localhost:8000/api/leads?producto_interes=Diseño&search=juan" \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por rango de fechas
curl "http://localhost:8000/api/leads?start_date=2024-01-01T00:00:00Z&end_date=2024-12-31T23:59:59Z" \
  -H "Authorization: Bearer $TOKEN"

# Obtener lead por ID
curl http://localhost:8000/api/leads/{id} \
  -H "Authorization: Bearer $TOKEN"

# Actualizar lead
curl -X PATCH http://localhost:8000/api/leads/{id} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"presupuesto":350.00}'

# Eliminar lead (soft delete - idempotente)
curl -X DELETE http://localhost:8000/api/leads/{id} \
  -H "Authorization: Bearer $TOKEN"
```

### Estadísticas

```bash
curl http://localhost:8000/api/leads/stats \
  -H "Authorization: Bearer $TOKEN"

# Respuesta:
# {
#   "success": true,
#   "data": {
#     "total": 150,
#     "por_fuente": {"instagram": 80, "facebook": 50, "landing_page": 20},
#     "promedio_presupuesto": 250.50,
#     "ultimos_7_dias": 25
#   }
# }
```

### AI Summary (Mock)

```bash
# Generar análisis de leads
curl -X POST http://localhost:8000/api/leads/ai/summary \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por fuente
curl -X POST "http://localhost:8000/api/leads/ai/summary?fuente=instagram" \
  -H "Authorization: Bearer $TOKEN"
```

### Webhook (público)

```bash
# Recebir leads desde sistemas externos
curl -X POST http://localhost:8000/api/leads/webhook \
  -H "Content-Type: application/json" \
  -d '{"nombre":"External Lead","email":"external@email.com","fuente":"facebook"}'
```

### Health Check

```bash
curl http://localhost:8000/health

# Respuesta:
# {"status": "healthy", "database": "connected", "version": "Lead Management API"}
```

## Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Variables de Entorno

Ver `.env.example` para todas las variables necesarias:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/leads_db

# JWT
JWT_SECRET_KEY=change-this-secret-key-min-32-characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
ENVIRONMENT=development
LOG_LEVEL=INFO

# CORS (lista blanca)
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

## Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Coverage
pytest --cov=app tests/ --cov-report=html
```

## Decisiones Técnicas

### ¿Por qué async?
PostgreSQL con asyncpg permite manejar miles de conexiones concurrentes sin I/O bloqueante.

### ¿Por qué Alembic?
Migraciones versionadas permiten rollback seguro y deployment reproducible.

### ¿Por qué Strategy Pattern en IA?
Permite cambiar de mock a OpenAI/Anthropic sin modificar código de negocio. La interfaz `AIServiceInterface` abstrae la implementación.

### ¿Por qué soft delete?
Preserva integridad referencial y permite auditoría histórica sin perder datos.

### ¿Por qué JWT stateless?
Escala horizontalmente sin necesidad de sesiones en memoria o Redis.

## License

MIT