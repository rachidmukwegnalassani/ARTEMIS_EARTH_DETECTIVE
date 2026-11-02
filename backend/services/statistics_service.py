# backend/services/statistics_service.py
from typing import Dict, Any, List
import numpy as np
from backend.utils.parsers import format_ui_table_for_llm

class StatisticsService:
    def __init__(self):
        pass

    def calculate_global_stats(self, raw_nasa_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcule les moyennes brutes, minimums, maximums et écarts-types 
        à partir des variables NASA reçues pour alimenter le tableau de l'UI.
        """
        if not raw_nasa_data:
            return {"headers": ["Métrique", "Valeur"], "rows": [["Données", "Aucune variable chargée"]]}

        try:
            values = [float(item['value']) for item in raw_nasa_data if item.get('value') is not None]
            
            if not values:
                return {"headers": ["Métrique", "Valeur"], "rows": [["Données", "Valeurs invalides"]]}

            mean_val = np.mean(values)
            max_val = np.max(values)
            min_val = np.min(values)
            std_dev = np.std(values)

            # Structure alignée avec les besoins de votre composant 'Statistiques Globales'
            return {
                "headers": ["Indicateur Statistique", "Valeur Calculée"],
                "rows": [
                    ["Moyenne Générale", f"{mean_val:.2f}"],
                    ["Maximum Détecté", f"{max_val:.2f}"],
                    ["Minimum Détecté", f"{min_val:.2f}"],
                    ["Écart-Type (Dispersion)", f"{std_dev:.2f}"],
                    ["Nombre de points analysés", str(len(values))]
                ]
            }
        except Exception as e:
            return {"headers": ["Erreur", "Message"], "rows": [["Calcul impossible", str(e)]]}

    def prepare_stats_context_for_ai(self, table_data: Dict[str, Any]) -> str:
        """
        Convertit les statistiques de l'UI en format Markdown lisible par Artemis 
        grâce au parser que nous avons créé.
        """
        return format_ui_table_for_llm(table_data)