# -*- coding: utf-8 -*-
# backend/schemas/dataset.py

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class DatasetBase(BaseModel):
    name: str = Field(..., example="MODIS Aqua - Sea Surface Temperature")
    description: Optional[str] = Field(None, example="Mesures quotidiennes de la température des océans")
    project: str = Field(..., example="Artemis Earth Detective")


class DatasetCreate(DatasetBase):
    pass


class DatasetResponse(DatasetBase):
    id: str = Field(..., example="MODIS_SST_L3")
    status: str = Field(..., example="available")
    details: Dict[str, Any]
