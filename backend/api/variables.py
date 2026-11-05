# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.api.chat import chat_engine

router = APIRouter(
    prefix="/variables",
    tags=["Variables"]
)

# Notre registre global structuré (Terre, Air, Eau, Glace)
NASA_VARIABLES_REGISTRY = {
    "terrestrial": {
        "label": "Milieu Terrestre & Biosphère",
        "items": {
            "ndvi": {"name": "NDVI (Indice de Végétation)", "unit": "Index (0 à 1)", "description": "Indice de vigueur de la végétation."},
            "forest_cover": {"name": "Couverture Forestière", "unit": "%", "description": "Densité de la canopée forestière."},
            "land_cover": {"name": "Occupation des Sols", "unit": "Classification", "description": "Type d'usage des sols."}
        }
    },
    "atmospheric": {
        "label": "Atmosphère & Climat",
        "items": {
            "surface_temp": {"name": "Température de Surface", "unit": "°C", "description": "Température de la surface terrestre."},
            "air_temp": {"name": "Température de l'Air", "unit": "°C", "description": "Température atmosphérique à 2m."},
            "humidity": {"name": "Humidité Relative", "unit": "%", "description": "Taux d'humidité dans l'air."},
            "precipitation": {"name": "Précipitations", "unit": "mm/h", "description": "Taux de chute de pluie ou neige."}
        }
    },
    "hydrological": {
        "label": "Hydrosphère & Cryosphère",
        "items": {
            "soil_moisture": {"name": "Humidité des Sols", "unit": "m³/m³", "description": "Quantité d'eau dans le sol."},
            "sea_level": {"name": "Niveau de la Mer", "unit": "mm", "description": "Fluctuation de la hauteur des océans."},
            "ice_thickness": {"name": "Épaisseur de la Glace", "unit": "mètres", "description": "Mesure de l'épaisseur de la banquise."}
        }
    }
}


class SelectVariableRequest(BaseModel):
    variable_id: str = Field(..., description="L'identifiant de la variable")


@router.get("/")
def get_variables():
    """Retourne le catalogue complet trié par milieu environnemental."""
    return {"status": "success", "categories": NASA_VARIABLES_REGISTRY}


# FUSION DE COPILOT : Route simplifiée pour lister uniquement les grands thèmes scientifiques
@router.get("/categories")
def get_categories_simple():
    """Retourne la liste simple des grands thèmes pour l'interface."""
    return {
        "categories": [
            "Atmosphere",
            "Hydrology",
            "Vegetation",
            "Ocean",
            "Cryosphere",
            "Land Cover"
        ]
    }


@router.post("/select")
def select_current_variable(data: SelectVariableRequest):
    """Met à jour la mémoire du gestionnaire de contexte de l'IA."""
    target_id = data.variable_id.lower().strip()
    found_variable = None
    found_category = None
    
    for cat_id, cat_data in NASA_VARIABLES_REGISTRY.items():
        if target_id in cat_data["items"]:
            found_variable = cat_data["items"][target_id]
            found_category = cat_data["label"]
            break
            
    if not found_variable:
        raise HTTPException(status_code=404, detail="Variable introuvable.")
        
    chat_engine.context.update_context({
        "current_variable": found_variable["name"],
        "current_environment": found_category
    })
    
    return {
        "status": "success",
        "context_sync": {"variable": found_variable["name"], "environment": found_category}
    }
