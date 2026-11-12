# -*- coding: utf-8 -*-

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

app = FastAPI(
    title="Artemis Earth Detective",
    description="Artificial Intelligence platform for Earth System Trend Detection and Analysis.",
    version="1.0.0"
) 

# Configuration CORS pour autoriser les requêtes de Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- ROUTE ESSENTIELLE POUR LE BOUTON DÉPLOYÉ ---
@app.get("/ping")
def ping_moteur():
    """
    Cette route intercepte le clic du bouton 'Accéder à l'application'.
    Elle réveille instantanément le serveur Render et valide la connexion
    pour charger les graphiques et le chatbot sans aucun terminal local.
    """
    return {
        "status": "online",
        "moteur": "Artemis Earth Detective",
        "message": "Connexion établie avec succès. Chargement des données NASA..."
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
# ==========================================================
# GESTION DU DASHBOARD GRAPHIQUE (Interface Utilisateur)
# ==========================================================

# BASE_DIR correspond à la racine de ton projet 'Artemis detective' sur Render
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Le chemin exact configuré selon l'arborescence réelle de ton GitHub
DASHBOARD_DIR = os.path.join(BASE_DIR, "frontend", "app-dashboard")

if os.path.exists(DASHBOARD_DIR):
    # On monte le dossier virtuel pour charger style.css, app.js, etc.
    app.mount("/interface", StaticFiles(directory=DASHBOARD_DIR), name="interface")

    # Route racine : Sert le fichier index.html de ton dossier 'frontend/app dashboard' !
    @app.get("/")
    def serve_dashboard():
        index_path = os.path.join(DASHBOARD_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {
            "application": "Artemis Earth Detective",
            "status": "online",
            "message": "index.html introuvable dans le dossier frontend/app dashboard"
        }
else:
    # Route de secours si le dossier n'est pas détecté au démarrage du serveur
    @app.get("/")
    def root_backup():
        return {
            "application": "Artemis Earth Detective",
            "status": "online",
            "warning": f"Le dossier attendu '{DASHBOARD_DIR}' n'a pas été détecté sur le serveur Render."
        }
        
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Moteur Artemis actif"}
