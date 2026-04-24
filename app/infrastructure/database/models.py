from sqlalchemy import Column, String, Boolean, Numeric, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database.connection import Base
import uuid
from datetime import datetime, timezone


class LeadModel(Base):
    __tablename__ = "leads"
    __table_args__ = (
        Index("ix_leads_fuente_created_at", "fuente", "created_at"),
        Index("ix_leads_is_deleted_fuente", "is_deleted", "fuente"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefono = Column(String(50))
    fuente = Column(String(50), nullable=False, index=True)
    producto_interes = Column(String(255))
    presupuesto = Column(Numeric(12, 2))
    is_deleted = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    rol = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)