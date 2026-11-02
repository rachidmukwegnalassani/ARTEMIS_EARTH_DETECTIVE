# backend/services/nasa_service.py
from typing import List, Dict, Any

class NasaService:
    def __init__(self):
        pass

    async def fetch_environmental_variables(self, dataset_id: str) -> List[Dict[str, Any]]:
        """
        Simule ou récupère les points de données des variables de la NASA.
        Retourne une liste de dictionnaires exploitables par le fichier de statistiques.
        """
        # Code d'intégration avec les API de la NASA
        # Exemple de structure renvoyée sans bloquer l'application :
        return [
            {"timestamp": "2026-11-02T12:00:00Z", "value": 24.5},
            {"timestamp": "2026-11-02T13:00:00Z", "value": 25.1}
        ]