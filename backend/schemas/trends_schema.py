# -*- coding: utf-8 -*-
# backend/schemas/trends_schema.py

from pydantic import BaseModel, Field


class TrendAnalysisSchema(BaseModel):
    intensity: str = Field(..., description="stable, modérée, significative, ou critique")
    direction: str = Field(..., description="up, down, or stable")
    explanation: str = Field(..., description="Phrase d'interprétation scientifique vulgarisée")
    status: str = Field(..., example="success")
