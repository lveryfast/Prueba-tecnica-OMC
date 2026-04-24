from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.lead import Lead


class AIServiceInterface(ABC):
    """Interface for AI services (mock or real implementation)."""
    
    @abstractmethod
    async def generate_summary(self, leads: List[Lead]) -> dict:
        """
        Generate lead summary analysis.
        
        Args:
            leads: List of leads to analyze
            
        Returns:
            dict with analysis:
                - fecha_analisis: ISO timestamp
                - total_leads: int
                - analisis: str with narrative
                - fuente_principal: str
                - distribucion_fuentes: dict
                - presupuesto_promedio: float
                - tendencia: str
                - recomendaciones: list[str]
        """
        pass