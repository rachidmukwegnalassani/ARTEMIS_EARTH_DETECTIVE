# backend/schemas/statistics_schema.py
from pydantic import BaseModel, Field
from typing import List, Any

class TableDataSchema(BaseModel):
    headers: List[str] = Field(..., example=["Indicateur Statistique", "Valeur Calculée"])
    rows: List[List[Any]] = Field(..., example=[["Moyenne Générale", "24.50"], ["Maximum Détecté", "31.20"]])

class LiveStatisticsResponseSchema(BaseModel):
    status: str
    calculated_indicators: int
    table: TableDataSchema