from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class User:
    id: Optional[UUID]
    email: str
    password_hash: str
    nombre: str
    rol: str = "user"
    is_active: bool = True