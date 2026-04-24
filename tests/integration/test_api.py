import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Lead Management API" in response.json()["message"]


@pytest.mark.asyncio
async def test_create_lead_validation_error(client):
    response = await client.post("/api/leads", json={
        "nombre": "J",
        "email": "invalid",
        "fuente": "invalid"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_lead_success(client):
    response = await client.post("/api/leads", json={
        "nombre": "Test User",
        "email": "test@example.com",
        "telefono": "+573012345678",
        "fuente": "instagram",
        "producto_interes": "Curso",
        "presupuesto": 299.99
    })
    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["nombre"] == "Test User"
    assert response.json()["data"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_leads_empty(client):
    response = await client.get("/api/leads")
    assert response.status_code == 200
    assert "success" in response.json()


@pytest.mark.asyncio
async def test_get_leads_with_filters(client):
    response = await client.get("/api/leads?page=1&limit=10&fuente=instagram")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "pages" in data


@pytest.mark.asyncio
async def test_get_leads_pagination(client):
    response = await client.get("/api/leads?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["page"] == 1
    assert data["limit"] == 5


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post("/api/auth/login", json={
        "email": "wrong@email.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_valid_credentials(client):
    response = await client.post("/api/auth/login", json={
        "email": "admin@leads.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_ai_summary(client):
    response = await client.post("/api/leads/ai/summary")
    assert response.status_code == 200
    assert "success" in response.json()


@pytest.mark.asyncio
async def test_webhook_lead(client):
    response = await client.post("/api/leads/webhook", json={
        "nombre": "Webhook Test",
        "email": "webhook@test.com",
        "fuente": "referido"
    })
    assert response.status_code == 201