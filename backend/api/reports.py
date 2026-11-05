# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.ai.report_generator import ReportGenerator
from backend.api.chat import chat_engine  # Synchronisation de la mémoire IA

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


class GenerateReportRequest(BaseModel):
    title: str = Field(..., description="Le titre personnalisé donné au rapport par l'utilisateur.")
    content_summary: str = Field(..., description="Notes additionnelles ou conclusions écrites par l'utilisateur ou l'IA.")


@router.get("/current")
def get_current_report_preview():
    """
    Génère un aperçu en direct du rapport Markdown basé sur les données actuellement 
    chargées dans le ContextManager de l'IA (sans écriture disque).
    """
    context = chat_engine.context
    if not getattr(context, "current_variable", None):
        raise HTTPException(
            status_code=400, 
            detail="Aucune enquête n'est active. Veuillez sélectionner une variable et analyser un fichier avant de générer un rapport."
        )

    # Extraction des données de contexte actuelles
    context_snapshot = {
        "current_environment": context.current_environment,
        "current_variable": context.current_variable,
        "current_period": context.current_period or "Période d'observation récente",
        "current_dataset": context.current_dataset or "Catalogue EarthData de la NASA",
        "current_statistics": context.current_statistics
    }

    # Génération du texte Markdown propre via notre ReportGenerator
    markdown_text = ReportGenerator.generate_markdown(
        title=f"Enquête sur {context.current_variable}",
        content="Aperçu automatique des données collectées par la constellation de satellites Artemis.",
        context_data=context_snapshot,
        timestamp_str="2026-11-04 (Format ISO)"  # Injection d'une chaîne fixe ou formatée conforme à l'architecture
    )

    return {
        "status": "success",
        "format": "markdown",
        "preview": markdown_text
    }


@router.post("/generate")
def generate_official_report(data: GenerateReportRequest):
    """
    Compile officiellement le rapport final et renvoie le document structuré,
    prêt pour l'affichage ordinateur ou un export de fichier.
    """
    context = chat_engine.context
    
    # Capture d'un instantané de la mémoire session
    context_snapshot = {
        "current_environment": context.current_environment,
        "current_variable": context.current_variable,
        "current_period": context.current_period,
        "current_dataset": context.current_dataset,
        "current_statistics": context.current_statistics
    }

    # Compilation via notre générateur d'architecture
    full_report_md = ReportGenerator.generate_markdown(
        title=data.title,
        content=data.content_summary,
        context_data=context_snapshot,
        timestamp_str="2026-11-04 16:00:00 UTC"
    )

    return {
        "status": "success",
        "filename": f"artemis_report_{data.title.lower().replace(' ', '_')}.md",
        "document_content": full_report_md
    }
