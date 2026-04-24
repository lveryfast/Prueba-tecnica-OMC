import pytest
from unittest.mock import AsyncMock
from app.domain.entities.lead import Lead
from app.application.dtos.lead_dto import CreateLeadDto, UpdateLeadDto
from app.application.use_cases.lead_use_cases import LeadUseCases


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def sample_lead():
    return Lead(
        id="12345678-1234-1234-1234-123456789012",
        nombre="Juan Perez",
        email="juan@email.com",
        telefono="+573012345678",
        fuente="instagram",
        producto_interes="Curso",
        presupuesto=299.99,
        is_deleted=False
    )


@pytest.mark.asyncio
async def test_create_lead_success(mock_repo, sample_lead):
    mock_repo.create = AsyncMock(return_value=sample_lead)
    
    use_cases = LeadUseCases(mock_repo)
    dto = CreateLeadDto(
        nombre="Juan Perez",
        email="juan@email.com",
        fuente="instagram"
    )
    
    result = await use_cases.create(dto)
    
    assert result.nombre == "Juan Perez"
    assert result.email == "juan@email.com"
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_lead_found(mock_repo, sample_lead):
    mock_repo.get_by_id = AsyncMock(return_value=sample_lead)
    
    use_cases = LeadUseCases(mock_repo)
    result = await use_cases.get("12345678-1234-1234-1234-123456789012")
    
    assert result is not None
    assert result.nombre == "Juan Perez"


@pytest.mark.asyncio
async def test_get_lead_not_found(mock_repo):
    mock_repo.get_by_id = AsyncMock(return_value=None)
    
    use_cases = LeadUseCases(mock_repo)
    result = await use_cases.get("nonexistent-id")
    
    assert result is None


@pytest.mark.asyncio
async def test_list_leads(mock_repo, sample_lead):
    mock_repo.get_all = AsyncMock(return_value=[sample_lead])
    
    use_cases = LeadUseCases(mock_repo)
    result = await use_cases.list(page=1, limit=10)
    
    assert len(result) == 1
    mock_repo.get_all.assert_called_once_with(1, 10)


@pytest.mark.asyncio
async def test_delete_lead_success(mock_repo):
    mock_repo.delete = AsyncMock(return_value=True)
    
    use_cases = LeadUseCases(mock_repo)
    result = await use_cases.delete("12345678-1234-1234-1234-123456789012")
    
    assert result is True


@pytest.mark.asyncio
async def test_stats(mock_repo):
    mock_repo.get_stats = AsyncMock(return_value={
        "total": 10,
        "por_fuente": {"instagram": 5, "facebook": 5},
        "promedio_presupuesto": 400.0,
        "ultimos_7_dias": 3
    })
    
    use_cases = LeadUseCases(mock_repo)
    result = await use_cases.stats()
    
    assert result["total"] == 10
    assert result["por_fuente"]["instagram"] == 5