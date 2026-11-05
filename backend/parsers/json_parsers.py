# -*- coding: utf-8 -*-

import json
from typing import Dict, Any


class JsonParser:

    @staticmethod
    def load_data(file_path: str) -> dict:
        """Charge un fichier JSON standard de manière sécurisée."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            return {"status": "success", "payload": content}
        except Exception as e:
            return {"status": "error", "message": f"Échec de l'analyse JSON : {str(e)}"}
