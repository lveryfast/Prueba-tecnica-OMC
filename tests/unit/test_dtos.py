import pytest
from app.application.dtos.lead_dto import CreateLeadDto, UpdateLeadDto
from app.application.dtos.auth_dto import LoginDto


def test_create_lead_dto_valid():
    dto = CreateLeadDto(
        nombre="Juan Perez",
        email="juan@email.com",
        telefono="+573012345678",
        fuente="instagram",
        producto_interes="Curso",
        presupuesto=299.99
    )
    assert dto.nombre == "Juan Perez"
    assert dto.email == "juan@email.com"
    assert dto.fuente == "instagram"


def test_create_lead_dto_invalid_fuente():
    with pytest.raises(ValueError):
        CreateLeadDto(
            nombre="Juan Perez",
            email="juan@email.com",
            fuente="invalid_source"
        )


def test_create_lead_dto_min_nombre():
    with pytest.raises(ValueError):
        CreateLeadDto(
            nombre="J",
            email="juan@email.com",
            fuente="instagram"
        )


def test_update_lead_dto_partial():
    dto = UpdateLeadDto(nombre="Nuevo Nombre")
    assert dto.nombre == "Nuevo Nombre"
    assert dto.email is None


def test_login_dto_valid():
    dto = LoginDto(
        email="admin@leads.com",
        password="admin123"
    )
    assert dto.email == "admin@leads.com"
    assert dto.password == "admin123"