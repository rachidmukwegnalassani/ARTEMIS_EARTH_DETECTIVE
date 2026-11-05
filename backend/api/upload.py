# -*- coding: utf-8 -*-

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.ai.file_analyzer import FileAnalyzer
from backend.api.chat import chat_engine  # Récupération de l'instance unique de notre Chat pour lier la mémoire

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# Dossier temporaire sécurisé pour analyser les fichiers de la NASA sur l'ordinateur
UPLOAD_DIR = os.path.join("backend", "temp_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_file(uploaded_file: UploadFile = File(...)):
    """
    Réceptionne un fichier scientifique ou géospatial de la NASA, l'enregistre localement,
    déclenche l'analyse automatique et synchronise le contexte de l'IA.
    """
    if not uploaded_file.filename:
        raise HTTPException(status_code=400, detail="Le fichier téléversé n'a pas de nom valide.")

    # 1. Analyse préliminaire de l'extension avec notre FileAnalyzer durci
    file_info = FileAnalyzer.detect_format(uploaded_file.filename)
    
    if not file_info["is_valid"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Format de fichier non supporté par Artemis : {file_info['extension']}"
        )

    # 2. Sécurisation et écriture du fichier sur le disque pour permettre aux moteurs de le lire
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
    try:
        with open(file_path, "wb") as buffer:
            # Lecture par morceaux pour éviter de saturer la mémoire RAM de l'ordinateur
            while content := await uploaded_file.read(1024 * 1024):
                buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Impossible d'enregistrer le fichier sur le serveur : {str(e)}")

    try:
        # 3. CRUCIAL : On envoie le fichier dans notre moteur de Chat persistant.
        # La méthode analyze_file va lire le fichier, lancer StatisticsAnalyzer et injecter les résultats dans le contexte.
        analysis_summary = chat_engine.analyze_file(file_path)
        
        # On nettoie le fichier temporaire après analyse si on ne souhaite pas encombrer le disque
        # os.remove(file_path) 

        return {
            "status": "success",
            "file_details": file_info,
            "engine_analysis": analysis_summary
        }

    except Exception as e:
        # Nettoyage de sécurité en cas de crash de lecture
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse interne du fichier : {str(e)}")
