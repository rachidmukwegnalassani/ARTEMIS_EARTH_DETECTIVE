# -*- coding: utf-8 -*-
# backend/schemas/charts_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChartQuerySchema(BaseModel):
    metric: str = Field(..., example="Air Temperature")
    start_date: str = Field(..., example="2026-01-01")
    end_date: str = Field(..., example="2026-11-02")
    chart_type: Optional[str] = Field("line", example="line")


class ChartResponseSchema(BaseModel):
    status: str = Field(..., example="success")
    count: int = Field(..., example=1)
    charts: List[Dict[str, Any]] = Field(default=[], description="Liste des configurations de graphiques de session")
