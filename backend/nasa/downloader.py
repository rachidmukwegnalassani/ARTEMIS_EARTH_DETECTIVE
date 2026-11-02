import os

class NasaDataDownloader:
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")

    def fetch_latest_dataset(self, variable_name: str) -> dict:
        """Simule la récupération sécurisée d'un lot de données de la NASA"""
        # En production, ce dictionnaire simule la réponse de l'API de la NASA
        return {
            "source": "NASA Earth Data Portal",
            "target_variable": variable_name,
            "status": "Ready",
            "file_meta": {
                "suggested_name": f"nasa_{variable_name}_latest.json",
                "format": "GeoJSON"
            }
        }