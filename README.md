# Lead Management API

API REST para gestión de leads con FastAPI + PostgreSQL.

## Stack

- **Python 3.11** + FastAPI
- **PostgreSQL** + SQLAlchemy async
- **JWT** para autenticación
- **Docker** + Docker Compose

## Installation

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno
cp .env.example .env
```

## Running

### Con Docker

```bash
docker-compose up --build
```

### Sin Docker

```bash
# PostgreSQL debe estar corriendo
uvicorn app.main:app --reload
```

## Endpoints

| Método | Endpoint | Descripción |
|-------|----------|-------------|
| POST | /api/leads | Crear lead |
| GET | /api/leads | Listar leads(paginado) |
| GET | /api/leads/{id} | Obtener lead |
| PATCH | /api/leads/{id} | Actualizar lead |
| DELETE | /api/leads/{id} | Eliminar lead(soft delete) |
| GET | /api/leads/stats | Estadísticas |
| POST | /api/auth/login | Login JWT |

## Auth

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@leads.com","password":"admin123"}'
```

## Seed

El init.sql crea 10 leads de ejemplo + usuario admin:
- Email: admin@leads.com
- Password: admin123

## Tests

```bash
pytest
```

## Docs

Swagger: http://localhost:8000/docs