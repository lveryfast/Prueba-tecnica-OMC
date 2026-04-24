from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.domain.entities.lead import Lead
from app.domain.interfaces.lead_repository import LeadRepositoryInterface
from app.infrastructure.database.models import LeadModel


class LeadRepository(LeadRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, lead: Lead) -> Lead:
        model = LeadModel(
            nombre=lead.nombre,
            email=lead.email,
            telefono=lead.telefono,
            fuente=lead.fuente,
            producto_interes=lead.producto_interes,
            presupuesto=lead.presupuesto
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, lead_id: UUID) -> Optional[Lead]:
        result = await self.session.execute(
            select(LeadModel).where(LeadModel.id == lead_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, page=1, limit=10) -> List[Lead]:
        result = await self.session.execute(
            select(LeadModel).where(LeadModel.is_deleted == False).offset((page-1)*limit).limit(limit)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def update(self, lead: Lead) -> Lead:
        result = await self.session.execute(
            select(LeadModel).where(LeadModel.id == lead.id)
        )
        model = result.scalar_one()
        model.nombre = lead.nombre
        model.email = lead.email
        model.telefono = lead.telefono
        model.fuente = lead.fuente
        model.producto_interes = lead.producto_interes
        model.presupuesto = lead.presupuesto
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, lead_id: UUID) -> bool:
        result = await self.session.execute(
            select(LeadModel).where(LeadModel.id == lead_id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.is_deleted = True
            await self.session.commit()
            return True
        return False

    async def get_stats(self) -> dict:
        leads = await self.get_all(page=1, limit=1000)
        
        total = len(leads)
        
        por_fuente = {}
        total_presupuesto = 0
        for lead in leads:
            por_fuente[lead.fuente] = por_fuente.get(lead.fuente, 0) + 1
            if lead.presupuesto:
                total_presupuesto += lead.presupuesto
        
        promedio = total_presupuesto / len(leads) if leads else 0
        ultimos_7 = len([l for l in leads if l.created_at and (datetime.utcnow() - l.created_at).days <= 7]) if leads else 0
        
        return {
            "total": total,
            "por_fuente": por_fuente,
            "promedio_presupuesto": round(promedio, 2),
            "ultimos_7_dias": ultimos_7
        }

    def _to_entity(self, model: LeadModel) -> Lead:
        return Lead(
            id=model.id,
            nombre=model.nombre,
            email=model.email,
            telefono=model.telefono,
            fuente=model.fuente,
            producto_interes=model.producto_interes,
            presupuesto=float(model.presupuesto) if model.presupuesto else None,
            is_deleted=model.is_deleted,
            created_at=model.created_at
        )