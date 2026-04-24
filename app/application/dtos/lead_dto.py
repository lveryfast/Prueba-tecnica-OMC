from pydantic import BaseModel, EmailStr, Field, field_validator

FUENTES = ("instagram", "facebook", "landing_page", "referido", "otro")


class CreateLeadDto(BaseModel):
    nombre: str = Field(..., min_length=2)
    email: EmailStr
    telefono: str | None = None
    fuente: str
    producto_interes: str | None = None
    presupuesto: float | None = None

    @field_validator("fuente")
    @classmethod
    def validate_fuente(cls, v):
        if v.lower() not in FUENTES:
            raise ValueError("Fuente inválida")
        return v.lower()


class UpdateLeadDto(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    fuente: str | None = None
    producto_interes: str | None = None
    presupuesto: float | None = None