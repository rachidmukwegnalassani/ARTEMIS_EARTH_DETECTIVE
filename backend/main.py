# -*- coding: utf-8 -*-
from fastapi import FastAPI

app = FastAPI(
    title="ARTEMIS Earth Detective API",
    version="1.0.0",
    description="Moteur d'Intelligence Spatiale Autonome - NASA Space Apps"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": "ARTEMIS",
        "message": "Le serveur de l'IA est fonctionnel et connecté à Render !"
    }