from sqlalchemy import Column, String, Boolean, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database.connection import Base
import uuid
from datetime import datetime


class LeadModel(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefono = Column(String(50))
    fuente = Column(String(50), nullable=False)
    producto_interes = Column(String(255))
    presupuesto = Column(Numeric(12, 2))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    rol = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)