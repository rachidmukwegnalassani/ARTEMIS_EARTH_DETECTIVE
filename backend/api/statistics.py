# -*- coding: utf-8 -*-

from fastapi import APIRouter
from backend.api.chat import chat_engine  # Synchronisation avec l'instance mémoire globale

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router.get("/")
def get_current_statistics():
    """
    Retourne dynamiquement les derniers indicateurs statistiques calculés 
    sur le fichier de la NASA actuellement chargé en mémoire.
    """
    # Extraction des statistiques stockées dans le ContextManager de l'IA
    current_stats = getattr(chat_engine.context, "current_statistics", {})

    if not current_stats:
        return {
            "status": "empty",
            "message": "Aucune donnée statistique n'est actuellement calculée. Veuillez charger un fichier.",
            "statistics": {}
        }

    return {
        "status": "success",
        "statistics": current_stats
    }


@router.get("/supported")
def supported_metrics():
    """
    Retourne la liste et la description des indicateurs statistiques 
    calculés par le moteur Pandas d'Artemis Earth Detective.
    """
    return {
        "status": "success",
        "metrics": [
            {"id": "mean", "label": "Moyenne Temporelle", "description": "Valeur centrale de la série de données de la NASA."},
            {"id": "median", "label": "Médiane", "description": "Point central séparant la moitié supérieure et inférieure des observations."},
            {"id": "std", "label": "Écart-Type (Dispersion)", "description": "Mesure l'étalement et la variabilité des anomalies climatiques."},
            {"id": "min", "label": "Valeur Minimale", "description": "Le seuil le plus bas enregistré sur la période."},
            {"id": "max", "label": "Valeur Maximale", "description": "Le pic le plus élevé enregistré sur la période."},
            {"id": "variance", "label": "Variance", "description": "Indicateur de la stabilité ou de la volatilité de la variable."},
            {"id": "p_value", "label": "Significativité (p-value)", "description": "Permet de valider scientifiquement si la tendance est réelle ou due au hasard."},
            {"id": "r_squared", "label": "Coefficient R²", "description": "Indique la fiabilité et la force du modèle d'évolution linéaire."}
        ]
    }
