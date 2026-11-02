# backend/schemas/reports_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ReportGenerationSchema(BaseModel):
    title: str = Field(..., example="Rapport d'Anomalie Climatique - Ray Detective")
    summary: str
    detected_anomalies: List[str] = []
    author: Optional[str] = Field("Artemis AI", example="Artemis AI")

class ExportConfigSchema(BaseModel):
    format: str = Field("txt", example="txt")
    include_history: bool = True