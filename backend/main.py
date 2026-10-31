# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse 
import os

app = FastAPI(
    title="ARTEMIS Earth Detective API",
    version="1.0.0",
    description="Moteur d'Intelligence Spatiale Autonome - NASA Space Apps"
)

@app.get("/")
async def read_root():
    return {
        "status": "online",
        "project": "ARTEMIS",
        "message": "Le serveur de l'IA est fonctionnel et connecté à Render !"
    }

# --- AJOUT DE LA PASSERELLE POUR LE DASHBOARD ---

# Indique à Render le chemin vers le dossier frontend global pour charger les fichiers CSS/JS
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Route directe pour afficher ton app-dashboard graphique sur Internet
@app.get("/app-dashboard")
async def ouvrir_dashboard():
    return FileResponse(os.path.join("frontend", "app-dashboard", "index.html"))