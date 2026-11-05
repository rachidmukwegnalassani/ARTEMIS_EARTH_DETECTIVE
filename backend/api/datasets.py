# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.api.chat import chat_engine  # Synchronisation de la mémoire IA

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)

# Registre des jeux de données réels de la NASA pertinents pour Artemis
NASA_DATASETS_REGISTRY = {
    "GPM_IMERG_V07": {
        "name": "Global Precipitation Measurement (GPM) - IMERG",
        "description": "Données mondiales de précipitations par satellite à haute résolution.",
        "resolution": "0.1° (~10km)",
        "temporal_range": "2000 - Présent"
    },
    "MODIS_SST_L3": {
        "name": "MODIS Aqua - Sea Surface Temperature (SST)",
        "description": "Mesures quotidiennes de la température de surface des océans par radiométrie infrarouge.",
        "resolution": "4km",
        "temporal_range": "2002 - Présent"
    },
    "SMAP_L4_SM": {
        "name": "Soil Moisture Active Passive (SMAP) - Level 4",
        "description": "Modélisation de l'humidité de surface et de la racine des sols à partir de données radar/radiomètre.",
        "resolution": "9km",
        "temporal_range": "2015 - Présent"
    }
}


class SelectDatasetRequest(BaseModel):
    dataset_id: str = Field(..., description="L'identifiant textuel du dataset de la NASA (ex: MODIS_SST_L3)")


@router.get("/")
def get_datasets():
    """
    Retourne la liste complète des jeux de données de la NASA supportés par Artemis.
    """
    return {
        "status": "success",
        "datasets": NASA_DATASETS_REGISTRY
    }


@router.get("/{dataset_id}")
def get_dataset(dataset_id: str):
    """
    Récupère les métadonnées spécifiques d'un jeu de données de la NASA.
    """
    uid = dataset_id.upper().strip()
    if uid not in NASA_DATASETS_REGISTRY:
        raise HTTPException(
            status_code=404, 
            detail=f"Jeu de données '{dataset_id}' introuvable dans le catalogue Artemis."
        )
    
    return {
        "id": uid,
        "status": "available",
        "details": NASA_DATASETS_REGISTRY[uid]
    }


@router.post("/select")
def select_current_dataset(data: SelectDatasetRequest):
    """
    Configure le dataset actif sur le dashboard et met à jour le ContextManager de l'IA.
    """
    uid = data.dataset_id.upper().strip()
    if uid not in NASA_DATASETS_REGISTRY:
        raise HTTPException(status_code=404, detail="Dataset introuvable.")
        
    target_dataset = NASA_DATASETS_REGISTRY[uid]
    
    # Synchronisation directe avec le ContextManager de l'IA
    chat_engine.context.update_context({
        "current_dataset": target_dataset["name"]
    })
    
    return {
        "status": "success",
        "message": f"Dataset de travail configuré sur : {target_dataset['name']}",
        "context_sync": {
            "dataset_name": target_dataset["name"]
        }
    }
