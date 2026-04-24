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
            select(LeadModel).offset((page-1)*limit).limit(limit)
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
        total = await self.session.scalar(select(func.count(LeadModel.id)))
        fuente = await self.session.execute(
            select(LeadModel.fuente, func.count(LeadModel.id)).group_by(LeadModel.fuente)
        )
        por_fuente = {f[0]: f[1] for f in fuente.all()}
        promedio = await self.session.scalar(select(func.avg(LeadModel.presupuesto)))
        siete = datetime.utcnow() - timedelta(days=7)
        ultimos = await self.session.scalar(
            select(func.count(LeadModel.id)).where(LeadModel.created_at >= siete)
        )
        return {"total": total, "por_fuente": por_fuente, "promedio_presupuesto": promedio or 0, "ultimos_7_dias": ultimos}

    def _to_entity(self, model: LeadModel) -> Lead:
        return Lead(
            id=model.id,
            nombre=model.nombre,
            email=model.email,
            telefono=model.telefono,
            fuente=model.fuente,
            producto_interes=model.producto_interes,
            presupuesto=float(model.presupuesto) if model.presupuesto else None,
            is_deleted=model.is_deleted
        )