from typing import List
from datetime import datetime, timezone
from app.domain.entities.lead import Lead
from app.domain.interfaces.ai_service import AIServiceInterface


class AIMockService(AIServiceInterface):
    async def generate_summary(self, leads: List[Lead]) -> dict:
        if not leads:
            return {
                "fecha_analisis": datetime.now(timezone.utc).isoformat(),
                "total_leads": 0,
                "analisis": "No hay leads para analizar",
                "fuente_principal": None,
                "distribucion_fuentes": {},
                "presupuesto_promedio": 0,
                "tendencia": "neutral",
                "recomendaciones": [
                    "Incrementar campañas de adquisición",
                    "Revisar efectividad de canales actuales"
                ]
            }

        fuente_mas = {}
        total_presupuesto = 0
        con_presupuesto = 0
        productos = {}

        for lead in leads:
            fuente_mas[lead.fuente] = fuente_mas.get(lead.fuente, 0) + 1
            if lead.presupuesto:
                total_presupuesto += lead.presupuesto
                con_presupuesto += 1
            if lead.producto_interes:
                productos[lead.producto_interes] = productos.get(lead.producto_interes, 0) + 1

        principal = max(fuente_mas, key=fuente_mas.get)
        promedio = total_presupuesto / con_presupuesto if con_presupuesto > 0 else 0
        producto_top = max(productos, key=productos.get) if productos else "N/A"

        return {
            "fecha_analisis": datetime.now(timezone.utc).isoformat(),
            "total_leads": len(leads),
            "analisis": f"Se analizaron {len(leads)} leads. La fuente principal es {principal} ({fuente_mas[principal]} leads). "
                        f"El interés principal es en {producto_top}. "
                        f"El presupuesto promedio es ${round(promedio, 2)} USD.",
            "fuente_principal": principal,
            "distribucion_fuentes": fuente_mas,
            "presupuesto_promedio": round(promedio, 2),
            "tendencia": "positiva" if promedio > 300 else "neutra" if promedio > 100 else "baja",
            "producto_mas_interes": producto_top,
            "recomendaciones": [
                f"Incrementar inversión en {principal} ({fuente_mas[principal]} leads)",
                f"Seguimiento prioritario a leads con presupuesto > ${round(promedio, 2)}",
                f"Desarrollar contenido sobre {producto_top}",
                "Implementar nurturing automatizado para leads fríos"
            ]
        }