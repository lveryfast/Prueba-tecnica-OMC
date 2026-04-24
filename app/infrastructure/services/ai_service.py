from typing import List
from app.domain.entities.lead import Lead


class AIMockService:
    async def generate_summary(self, leads: List[Lead]) -> dict:
        if not leads:
            return {"analisis": "No hay leads", "recomendaciones": []}

        fuente_mas = {}
        total_presupuesto = 0
        for lead in leads:
            fuente_mas[lead.fuente] = fuente_mas.get(lead.fuente, 0) + 1
            if lead.presupuesto:
                total_presupuesto += lead.presupuesto

        principal = max(fuente_mas, key=fuente_mas.get)
        promedio = total_presupuesto / len(leads)

        return {
            "analisis": f"Análisis de {len(leads)} leads. Fuente principal: {principal}",
            "fuente_principal": principal,
            "presupuesto_promedio": round(promedio, 2),
            "recomendaciones": [f"Invertir en {principal}", f"Seguimiento a presupuesto > ${round(promedio,2)}"]
        }