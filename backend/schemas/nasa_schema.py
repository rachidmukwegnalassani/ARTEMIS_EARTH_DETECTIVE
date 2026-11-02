# backend/schemas/nasa_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional

class NasaDataPointSchema(BaseModel):
    timestamp: str = Field(..., example="2026-11-02T22:57:00Z")
    value: float = Field(..., example=24.5)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class NasaVariableRequestSchema(BaseModel):
    variable_name: str = Field(..., example="Air_Temp_A")
    resolution: str = Field("daily", example="daily")