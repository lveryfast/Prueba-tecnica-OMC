from typing import Optional, List
from datetime import datetime
from uuid import UUID
from typing import Literal

from app.domain.entities.lead import Lead
from app.domain.interfaces.lead_repository import LeadRepositoryInterface
from app.application.dtos.lead_dto import CreateLeadDto, UpdateLeadDto

SortableFields = Literal["created_at", "nombre", "email", "fuente", "presupuesto"]
SortOrder = Literal["asc", "desc"]


class LeadUseCases:
    def __init__(self, repo: LeadRepositoryInterface):
        self.repo = repo

    async def create(self, dto: CreateLeadDto) -> Lead:
        existing = await self.repo.get_by_email(dto.email)
        if existing:
            raise ValueError(f"El email {dto.email} ya está registrado")
        
        lead = Lead(
            id=None,
            nombre=dto.nombre,
            email=dto.email,
            telefono=dto.telefono,
            fuente=dto.fuente,
            producto_interes=dto.producto_interes,
            presupuesto=dto.presupuesto
        )
        return await self.repo.create(lead)

    async def get(self, lead_id: str) -> Optional[Lead]:
        return await self.repo.get_by_id(UUID(lead_id))

    async def list(
        self,
        page: int = 1,
        limit: int = 10,
        fuente: Optional[str] = None,
        producto_interes: Optional[str] = None,
        search: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        sort_by: Optional[SortableFields] = "created_at",
        sort_order: SortOrder = "desc"
) -> dict:
        leads = await self.repo.get_all(
            page, limit, fuente, produto_interes, search, start_date, end_date, sort_by, sort_order
        )
        total = await self.repo.count(fuente, produto_interes, search, start_date, end_date)
        pages = (total + limit - 1) // limit if limit > 0 else 0
        
        return {
            "items": leads,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages
        }

    async def update(self, lead_id: str, dto: UpdateLeadDto) -> Lead:
        lead = await self.repo.get_by_id(UUID(lead_id))
        if not lead:
            raise ValueError("Lead no encontrado")
        
        if dto.nombre: lead.nombre = dto.nombre
        if dto.email: lead.email = dto.email
        if dto.telefono is not None: lead.telefono = dto.telefono
        if dto.fuente: lead.fuente = dto.fuente
        if dto.producto_interes is not None: lead.producto_interes = dto.producto_interes
        if dto.presupuesto is not None: lead.presupuesto = dto.presupuesto
            
        return await self.repo.update(lead)

    async def delete(self, lead_id: str) -> bool:
        return await self.repo.delete(UUID(lead_id))

    async def stats(self) -> dict:
        return await self.repo.get_stats()