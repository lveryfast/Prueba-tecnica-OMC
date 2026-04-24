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

    async def get_by_email(self, email: str) -> Optional[Lead]:
        result = await self.session.execute(
            select(LeadModel).where(LeadModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        fuente: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Lead]:
        query = select(LeadModel).where(LeadModel.is_deleted == False)
        
        if fuente:
            query = query.where(LeadModel.fuente == fuente)
        if start_date:
            query = query.where(LeadModel.created_at >= start_date)
        if end_date:
            query = query.where(LeadModel.created_at <= end_date)
        
        query = query.order_by(LeadModel.created_at.desc())
        query = query.offset((page - 1) * limit).limit(limit)
        
        result = await self.session.execute(query)
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

    async def count(
        self,
        fuente: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        query = select(func.count(LeadModel.id)).where(LeadModel.is_deleted == False)
        
        if fuente:
            query = query.where(LeadModel.fuente == fuente)
        if start_date:
            query = query.where(LeadModel.created_at >= start_date)
        if end_date:
            query = query.where(LeadModel.created_at <= end_date)
        
        result = await self.session.scalar(query)
        return result or 0

    async def get_stats(self) -> dict:
        total = await self.count()
        
        fuente_result = await self.session.execute(
            select(LeadModel.fuente, func.count(LeadModel.id))
            .where(LeadModel.is_deleted == False)
            .group_by(LeadModel.fuente)
        )
        por_fuente = {row[0]: row[1] for row in fuente_result.all()}
        
        avg_result = await self.session.scalar(
            select(func.avg(LeadModel.presupuesto)).where(LeadModel.is_deleted == False)
        )
        promedio = float(avg_result) if avg_result else 0
        
        siete = datetime.utcnow() - timedelta(days=7)
        ultimos = await self.session.scalar(
            select(func.count(LeadModel.id))
            .where(LeadModel.is_deleted == False)
            .where(LeadModel.created_at >= siete)
        )
        
        return {
            "total": total,
            "por_fuente": por_fuente,
            "promedio_presupuesto": round(promedio, 2),
            "ultimos_7_dias": ultimos or 0
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