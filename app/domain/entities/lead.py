from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Lead:
    id: Optional[UUID]
    nombre: str
    email: str
    telefono: Optional[str]
    fuente: str
    producto_interes: Optional[str]
    presupuesto: Optional[float]
    is_deleted: bool = False
    created_at: Optional[datetime] = None