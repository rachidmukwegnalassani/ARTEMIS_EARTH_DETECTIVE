# backend/schemas/charts_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ChartQuerySchema(BaseModel):
    metric: str = Field(..., example="Air Temperature")
    start_date: str = Field(..., example="2026-01-01")
    end_date: str = Field(..., example="2026-11-02")
    chart_type: Optional[str] = Field("line", example="line")

class ChartDatasetElement(BaseModel):
    label: str
    data: List[float]
    borderColor: str
    backgroundColor: str
    fill: bool

class ChartResponseSchema(BaseModel):
    labels: List[str]
    datasets: List[ChartDatasetElement]