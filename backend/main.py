# -*- coding: utf-8 -*-

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Importation de nos routes d'API durcies
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
    description="Artificial Intelligence platform for Earth System Trend Detection and Analysis.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuration CORS pour autoriser les requêtes de Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# ==========================================================
# GESTION DU DASHBOARD GRAPHIQUE (Interface Utilisateur)
# ==========================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FRONTEND_CANDIDATES = [
    os.path.join(BASE_DIR, "frontend", "app-dashboard"),
    os.path.join(BASE_DIR, "frontend", "app dashboard"),
    os.path.join(BASE_DIR, "frontend"),
]

DASHBOARD_DIR = next((path for path in FRONTEND_CANDIDATES if os.path.isdir(path)), None)

if DASHBOARD_DIR:
    app.mount("/interface", StaticFiles(directory=DASHBOARD_DIR), name="interface")

    @app.get("/")
    def serve_dashboard():
        index_path = os.path.join(DASHBOARD_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"application": "Artemis Earth Detective", "status": "online", "message": "index.html introuvable dans le dossier frontend."}
else:
    @app.get("/")
    def root_backup():
        return {
            "application": "Artemis Earth Detective",
            "status": "online",
            "warning": "Le dossier frontend n'a pas été détecté sur le serveur.",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=APP_HOST, port=APP_PORT, reload=True)
