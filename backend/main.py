# -*- coding: utf-8 -*-

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importation de toutes nos routes d'API durcies et synchronisées
from backend.api.health import router as health_router
from backend.api.variables import router as variables_router
from backend.api.datasets import router as datasets_router
from backend.api.upload import router as upload_router
from backend.api.charts import router as charts_router
from backend.api.statistics import router as statistics_router
from backend.api.trends import router as trends_router
from backend.api.reports import router as reports_router
from backend.api.chat import router as chat_router

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("PORT", os.getenv("APP_PORT", "8000")))

app = FastAPI(
    title="Artemis Earth Detective",
    description=(
        "Artificial Intelligence platform for "
        "Earth System Trend Detection and Analysis."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ==========================================================
# CONFIGURATION CORS (Indispensable pour l'affichage de l'UI)
# ==========================================================
# Permet à ton tableau de bord frontend de communiquer librement avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les requêtes (idéal pour le développement sur ton PC)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise le POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():
    return {
        "application": "Artemis Earth Detective",
        "status": "online",
        "version": "1.0.0"
    }


# ==========================================================
# API ROUTERS (Liaison officielle des modules)
# ==========================================================

app.include_router(health_router)
app.include_router(variables_router)
app.include_router(datasets_router)
app.include_router(upload_router)
app.include_router(charts_router)
app.include_router(statistics_router)
app.include_router(trends_router)
app.include_router(reports_router)
app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=True,
    )
