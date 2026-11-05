# -*- coding: utf-8 -*-

import os
from fastapi import APIRouter, Response, status
from backend.api.chat import chat_engine  # Vérification de l'état de la mémoire globale

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check(response: Response):
    """
    Effectue un diagnostic complet du backend Artemis Earth Detective.
    Vérifie la disponibilité des répertoires et l'intégrité de la mémoire IA.
    """
    health_status = {
        "status": "healthy",
        "service": "Artemis Earth Detective Backend",
        "version": "1.0.0",
        "checks": {
            "ai_memory_engine": "unknown",
            "storage_system": "unknown"
        }
    }

    # 1. Vérification de l'intégrité du moteur de contexte de l'IA
    if chat_engine and hasattr(chat_engine, "context"):
        health_status["checks"]["ai_memory_engine"] = "operational"
    else:
        health_status["checks"]["ai_memory_engine"] = "corrupted"
        health_status["status"] = "degraded"

    # 2. Vérification des accès au système de fichiers (dossier temporaire d'upload de la NASA)
    upload_dir = os.path.join("backend", "temp_uploads")
    if os.path.exists(upload_dir) and os.access(upload_dir, os.W_OK):
        health_status["checks"]["storage_system"] = "writable"
    else:
        health_status["checks"]["storage_system"] = "read-only / inaccessible"
        health_status["status"] = "degraded"

    # Modification dynamique du code HTTP si le service est dégradé pour alerter les moniteurs cloud
    if health_status["status"] == "degraded":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return health_status
