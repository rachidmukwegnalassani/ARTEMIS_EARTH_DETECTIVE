# backend/schemas/trends_schema.py
from pydantic import BaseModel, Field
from typing import Optional

class TrendAnalysisSchema(BaseModel):
    metric: str
    percentage_change: float = Field(..., description="Taux d'évolution calculé")
    direction: str = Field(..., description="up, down, or stable")
    is_anomaly: bool = False
    confidence_score: Optional[float] = 0.95