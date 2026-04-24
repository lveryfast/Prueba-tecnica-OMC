import pytest
from unittest.mock import AsyncMock
from uuid import UUID
from app.domain.entities.lead import Lead
from app.application.dtos.lead_dto import CreateLeadDto, UpdateLeadDto
from app.application.use_cases.lead_use_cases import LeadUseCases


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def sample_lead():
    return Lead(
        id=UUID("12345678-1234-1234-1234-123456789012"),
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
    mock_repo.get_by_email = AsyncMock(return_value=None)
    mock_repo.create = AsyncMock(return_value=sample_lead)
    
    use_cases = LeadUseCases(mock_repo)
    dto = CreateLeadDto(
        nombre="Juan Perez",
        email="juan@email.com",
        fuente="instagram"
    )
    
    result = await use_cases.create(dto)
    
    assert result.nombre == "Juan Perez"
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_lead_duplicate_email(mock_repo):
    mock_repo.get_by_email = AsyncMock(return_value=Lead(
        id=UUID("12345678-1234-1234-1234-123456789012"),
        nombre="Existing",
        email="existing@email.com",
        telefono=None,
        fuente="instagram",
        producto_interes=None,
        presupuesto=None
    ))
    
    use_cases = LeadUseCases(mock_repo)
    dto = CreateLeadDto(
        nombre="Juan Perez",
        email="existing@email.com",
        fuente="instagram"
    )
    
    with pytest.raises(ValueError, match="ya está registrado"):
        await use_cases.create(dto)


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
    result = await use_cases.get("12345678-1234-1234-1234-123456789012")
    
    assert result is None


@pytest.mark.asyncio
async def test_list_leads_with_pagination(mock_repo, sample_lead):
    mock_repo.get_all = AsyncMock(return_value=[sample_lead])
    mock_repo.count = AsyncMock(return_value=1)
    
    use_cases = LeadUseCases(mock_repo)
    result = await use_cases.list(page=1, limit=10)
    
    assert "items" in result
    assert "total" in result
    assert "page" in result
    assert "pages" in result
    assert result["total"] == 1
    # New signature: page, limit, fuente, producto_interes, search, start_date, end_date, sort_by, sort_order
    mock_repo.get_all.assert_called_once_with(1, 10, None, None, None, None, None, "created_at", "desc")


@pytest.mark.asyncio
async def test_list_leads_with_filters(mock_repo, sample_lead):
    mock_repo.get_all = AsyncMock(return_value=[sample_lead])
    mock_repo.count = AsyncMock(return_value=1)
    
    use_cases = LeadUseCases(mock_repo)
    result = await use_cases.list(page=1, limit=10, fuente="instagram")
    
    assert result["total"] == 1
    mock_repo.get_all.assert_called_once_with(1, 10, "instagram", None, None, None, None, "created_at", "desc")


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