# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 1. Configurer le dossier pour vos fichiers statiques (CSS, JS, images)
# Assurez-vous que le chemin pointe bien vers votre dossier "app-dashboard"
app.mount("/static", StaticFiles(directory="frontend/app-dashboard"), name="static")

# 2. Forcer la racine à charger l'interface visuelle (HTML)
@app.get("/")
def read_root():
    # Ajustez le chemin selon l'emplacement exact de votre index.html
    return FileResponse(os.path.join("frontend", "app-dashboard", "index.html"))
# --- AJOUT DE LA PASSERELLE POUR LE DASHBOARD ---

# Indique à Render le chemin vers le dossier frontend global pour charger les fichiers CSS/JS
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Route directe pour afficher ton app-dashboard graphique sur Internet
@app.get("/app-dashboard")
async def ouvrir_dashboard():
    return FileResponse(os.path.join("frontend", "app-dashboard", "index.html"))