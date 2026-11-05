# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.ai.explanation_engine import ExplanationEngine
from backend.api.chat import chat_engine  # Synchronisation de la mémoire IA

router = APIRouter(
    prefix="/trends",
    tags=["Trend Analysis"]
)


class TrendAnalysisRequest(BaseModel):
    trend_value: float = Field(..., description="Le facteur de pente ou coefficient de tendance calculé sur la série.")


@router.get("/")
def get_current_trend():
    """
    Récupère la tendance actuellement stockée en mémoire dans le contexte de l'IA.
    """
    context = chat_engine.context
    variable = getattr(context, "current_variable", "Variable non définie")
    
    # On tente de récupérer des calculs statistiques en cours
    stats = getattr(context, "current_statistics", {})
    mean_change = stats.get("mean_change") or stats.get("mean", 0.0)

    # Génération d'une explication à la volée basée sur l'état de la mémoire
    analysis = ExplanationEngine.explain_trend(mean_change, variable)

    return {
        "status": "success",
        "current_monitored_variable": variable,
        "analysis": analysis
    }


@router.post("/analyze")
def analyze_trend(data: TrendAnalysisRequest):
    """
    Analyse instantanément une valeur de tendance, qualifie son intensité environnementale
    et met à jour les conclusions lues par le Chat IA d'Artemis.
    """
    try:
        # Récupération de la variable active dans le chat pour contextualiser l'explication
        active_variable = getattr(chat_engine.context, "current_variable", "Indicateur NASA")

        # Calcul de l'explication scientifique via notre ExplanationEngine Pandas
        trend_analysis = ExplanationEngine.explain_trend(data.trend_value, active_variable)

        # Injection de cette conclusion dans la mémoire persistante du chat
        if "current_statistics" in chat_engine.context.__dict__:
            chat_engine.context.current_statistics["interpretation"] = trend_analysis["explanation"]

        return {
            "status": "success",
            "trend_value": data.trend_value,
            "variable_context": active_variable,
            "interpretation": trend_analysis
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'exécution du moteur de tendance : {str(e)}"
        )
