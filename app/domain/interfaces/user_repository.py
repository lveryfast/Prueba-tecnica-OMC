from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        pass