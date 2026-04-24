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
async def test_health_endpoint(client):
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
        "email": "invalid-email",
        " fuente": "invalid"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_leads_empty(client):
    response = await client.get("/api/leads")
    assert response.status_code == 200
    assert "success" in response.json()