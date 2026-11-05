# -*- coding: utf-8 -*-
# backend/schemas/reports_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional


class ReportGenerationSchema(BaseModel):
    title: str = Field(..., example="Rapport d'Anomalie Climatique")
    content_summary: str = Field(..., description="Résumé textuel ou conclusions scientifiques.")


class ExportConfigSchema(BaseModel):
    format: str = Field("markdown", example="markdown")
    include_history: bool = True
