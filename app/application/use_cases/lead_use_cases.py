from app.domain.entities.lead import Lead
from app.domain.interfaces.lead_repository import LeadRepositoryInterface
from app.application.dtos.lead_dto import CreateLeadDto, UpdateLeadDto


class LeadUseCases:
    def __init__(self, repo: LeadRepositoryInterface):
        self.repo = repo

    async def create(self, dto: CreateLeadDto) -> Lead:
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

    async def get(self, lead_id: str):
        return await self.repo.get_by_id(lead_id)

    async def list(self, page=1, limit=10):
        return await self.repo.get_all(page, limit)

    async def update(self, lead_id: str, dto: UpdateLeadDto):
        lead = await self.repo.get_by_id(lead_id)
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
        return await self.repo.delete(lead_id)

    async def stats(self) -> dict:
        return await self.repo.get_stats()