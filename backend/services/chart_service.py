# backend/services/chart_service.py
from typing import List, Dict, Any
from backend.utils.time_helpers import filter_time_series_by_range, format_timestamp_for_ui

class ChartService:
    def __init__(self):
        pass

    def prepare_nasa_chart_data(self, raw_data: List[Dict[str, Any]], start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Filtre et convertit les données environnementales brutes de la NASA 
        en un format exploitable par Chart.js ou Plotly sur l'interface utilisateur.
        """
        filtered_points = filter_time_series_by_range(raw_data, start_date, end_date)
        
        # Extraction des labels temporels et des valeurs scientifiques
        labels = [format_timestamp_for_ui(pt.get("timestamp", "")) for pt in filtered_points]
        values = [float(pt.get("value", 0.0)) for pt in filtered_points]
        
        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Évolution de la variable environnementale",
                    "data": values,
                    "borderColor": "#4A90E2",
                    "backgroundColor": "rgba(74, 144, 226, 0.2)",
                    "fill": True
                }
            ]
        }