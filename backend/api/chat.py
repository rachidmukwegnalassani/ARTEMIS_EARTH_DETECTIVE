import shutil
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from backend.ai.scientific_chat import ScientificChat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

chat_engine = ScientificChat()
UPLOAD_DIR = Path("backend/temp-uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class ChatRequest(BaseModel):
    message: str = Field(..., description="Le message ou la question de l'utilisateur pour l'IA d'Artemis")


@router.post("/upload")
async def upload_chat_file(file: UploadFile = File(...)):
    try: 
        if not file.filename:
            raise HTTPException(status_code=400, detail="Aucun fichier n'a été fourni pour l'analyse.")
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = chat_engine.analyze_file(str(file_path))
        return {
            "status": "success",
            "message": f"Fichier '{file.filename}' analysé ({result['variable']}). Vous pouvez maintenant me poser des questions sur ces données.",
            "details": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Impossible d'analyser le fichier : {str(e)}")


@router.post("/send_message")
def send_message(data: ChatRequest):
    try:
        if not data.message.strip():
            raise HTTPException(status_code=400, detail="Le message ne peut pas être vide.")

        analysis_result = chat_engine.answer_question(data.message)
        return {
            "status": "success",
            "reply": analysis_result,
            "response": analysis_result,
            "analysis_result": analysis_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne Artemis IA : {str(e)}")


@router.get("/capabilities")
def get_capabilities():
    return {
        "status": "success",
        "supported_formats": [
            "GeoJSON",
            "Shapefile (SHP)",
            "GeoTIFF (TIF/TIFF)",
            "NetCDF (NC)",
            "HDF (HDF4/HDF5)",
            "CSV",
            "XLSX"
        ]
    }