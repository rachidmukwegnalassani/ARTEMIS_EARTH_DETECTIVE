import json

class JsonParser:
    @staticmethod
    def load_data(file_path: str) -> dict:
        """Charge et désérialise de manière sécurisée tout fichier au format JSON standard"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            return {
                "status": "success",
                "payload": content
            }
        except Exception as e:
            return {"status": "error", "message": f"Échec de l'analyse JSON : {str(e)}"}