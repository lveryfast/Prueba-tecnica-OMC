from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.lead_repository import LeadRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.services.auth_service import AuthService
from app.infrastructure.services.ai_service import AIMockService
from app.application.dtos.lead_dto import CreateLeadDto, UpdateLeadDto
from app.application.dtos.auth_dto import LoginDto, LoginResponseDto
from app.application.use_cases.lead_use_cases import LeadUseCases
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.config import settings


router = APIRouter()
auth_service = AuthService()
ai_service = AIMockService()


@router.post("/leads", status_code=201)
async def create_lead(dto: CreateLeadDto, db: AsyncSession = Depends(get_db)):
    repo = LeadRepository(db)
    use_cases = LeadUseCases(repo)
    try:
        lead = await use_cases.create(dto)
        return {"success": True, "data": lead}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leads")
async def list_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    fuente: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    repo = LeadRepository(db)
    use_cases = LeadUseCases(repo)
    result = await use_cases.list(page, limit, fuente, start_date, end_date)
    return {"success": True, "data": result}


@router.get("/leads/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    repo = LeadRepository(db)
    use_cases = LeadUseCases(repo)
    return {"success": True, "data": await use_cases.stats()}


@router.post("/leads/ai/summary")
async def ai_summary(fuente: str = None, db: AsyncSession = Depends(get_db)):
    repo = LeadRepository(db)
    leads = await repo.get_all(page=1, limit=100, fuente=fuente)
    summary = await ai_service.generate_summary(leads)
    return {"success": True, "data": summary}


@router.post("/leads/webhook")
async def webhook_lead(dto: CreateLeadDto, db: AsyncSession = Depends(get_db)):
    repo = LeadRepository(db)
    use_cases = LeadUseCases(repo)
    try:
        lead = await use_cases.create(dto)
        return {"success": True, "message": "Lead recibido desde webhook", "lead_id": str(lead.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leads/{lead_id}")
async def get_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    repo = LeadRepository(db)
    use_cases = LeadUseCases(repo)
    lead = await use_cases.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"success": True, "data": lead}


@router.patch("/leads/{lead_id}")
async def update_lead(lead_id: str, dto: UpdateLeadDto, db: AsyncSession = Depends(get_db)):
    repo = LeadRepository(db)
    use_cases = LeadUseCases(repo)
    try:
        lead = await use_cases.update(lead_id, dto)
        return {"success": True, "data": lead}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/leads/{lead_id}")
async def delete_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    repo = LeadRepository(db)
    use_cases = LeadUseCases(repo)
    result = await use_cases.delete(lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return {"success": True, "message": "Lead eliminado"}


@router.post("/auth/login")
async def login(dto: LoginDto, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    use_cases = AuthUseCases(user_repo)
    try:
        user = await use_cases.login(dto)
        token = auth_service.create_access_token(user.email, user.rol)
        return LoginResponseDto(
            access_token=token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={"email": user.email, "nombre": user.nombre, "rol": user.rol}
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))