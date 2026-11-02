# backend/services/export_service.py
from typing import Dict, Any
import io

class ExportService:
    def __init__(self):
        pass

    def export_analysis_to_txt(self, session_chat: list) -> io.BytesIO:
        """
        Compile l'historique des analyses scientifiques croisées d'Artemis 
        dans un fichier texte téléchargeable pour l'analyste.
        """
        output = io.BytesIO()
        text_content = "=== RAPPORT D'ANALYSE SCIENTIFIQUE - ARTEMIS RAY DETECTIVE ===\n\n"
        
        for message in session_chat:
            role = "Artemis (IA)" if message.get("role") == "assistant" else "Analyste (User)"
            text_content += f"[{role}] :\n{message.get('content')}\n"
            text_content += "-" * 50 + "\n"
            
        output.write(text_content.encode('utf-8'))
        output.seek(0)
        return output