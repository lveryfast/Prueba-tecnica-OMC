from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.lead import Lead


class LeadRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, lead: Lead) -> Lead:
        pass
    
    @abstractmethod
    async def get_by_id(self, lead_id: UUID) -> Optional[Lead]:
        pass
    
    @abstractmethod
    async def get_all(self, page: int = 1, limit: int = 10) -> List[Lead]:
        pass
    
    @abstractmethod
    async def update(self, lead: Lead) -> Lead:
        pass
    
    @abstractmethod
    async def delete(self, lead_id: UUID) -> bool:
        pass
    
    @abstractmethod
    async def get_stats(self) -> dict:
        pass