# -*- coding: utf-8 -*-

from fastapi import APIRouter
from backend.api.chat import chat_engine  # Récupération de l'instance mémoire globale d'Artemis

router = APIRouter(
    prefix="/charts",
    tags=["Charts"]
)


@router.get("/")
def get_charts():
    """
    Retourne dynamiquement la liste des graphiques générés pour l'enquête en cours.
    Ces données proviennent directement du ContextManager de notre IA.
    """
    # Extraction des graphiques stockés en mémoire session
    current_session_charts = getattr(chat_engine.context, "current_charts", [])

    return {
        "status": "success",
        "count": len(current_session_charts),
        "charts": current_session_charts
    }


@router.get("/supported")
def supported_charts():
    """
    Retourne la liste des types de graphiques supportés par le moteur
    de rendu d'Artemis pour l'affichage sur ordinateur (Chart.js / Plotly).
    """
    return {
        "status": "success",
        "types": [
            {"id": "line", "label": "Courbe de Tendance", "description": "Idéal pour observer l'évolution globale d'une variable."},
            {"id": "timeseries", "label": "Série Chronologique", "description": "Recommandé pour les cycles climatiques et temporels de la NASA."},
            {"id": "bar", "label": "Histogramme à Barres", "description": "Utile pour comparer des moyennes par périodes ou par zones."},
            {"id": "scatter", "label": "Nuage de Points", "description": "Idéal pour croiser deux variables environnementales (ex: CO2 vs Température)."},
            {"id": "histogram", "label": "Distribution", "description": "Affiche la répartition spectrale ou statistique des mesures."}
        ]
    }
