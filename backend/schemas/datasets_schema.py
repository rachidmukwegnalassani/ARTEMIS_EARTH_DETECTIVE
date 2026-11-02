# backend/schemas/dataset.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class DatasetBase(BaseModel):
    name: str = Field(..., example="Anomalies Thermiques Gabon")
    description: Optional[str] = Field(None, example="Données composites issues de la NASA")
    project: str = Field(..., example="Artemis Earth Detective")  # Assure la compatibilité avec les routes

class DatasetCreate(DatasetBase):
    pass

class DatasetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project: Optional[str] = None

class DatasetResponse(DatasetBase):
    id: int
    filename: str
    file_path: str
    metadata_fields: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True  # Permet de lire directement les objets de la base de données (ORMs)