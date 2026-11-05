# -*- coding: utf-8 -*-
# backend/schemas/statistics_schema.py

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class TableDataSchema(BaseModel):
    count: int = Field(..., example=120)
    mean: float = Field(..., example=24.50)
    median: float = Field(..., example=24.20)
    minimum: float = Field(..., example=12.10)
    maximum: float = Field(..., example=35.60)
    std: float = Field(..., example=2.15)
    interpretation: Optional[str] = Field(None, example="La tendance observée est statistiquement significative.")


class LiveStatisticsResponseSchema(BaseModel):
    status: str = Field(..., example="success")
    statistics: TableDataSchema
