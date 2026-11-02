# backend/services/map_service.py
from typing import Dict, Any, List
from backend.utils.geo_helpers import calculate_bounding_box, validate_geojson

class MapService:
    def __init__(self):
        pass

    def prepare_map_layer(self, geojson_data: Dict[str, Any], layer_name: str) -> Dict[str, Any]:
        """
        Valide et configure une couche cartographique pour l'interface de carte Leaflet/Mapbox.
        """
        if not validate_geojson(geojson_data):
            return {"status": "error", "message": "Fichier géospatial GeoJSON invalide ou corrompu."}
            
        # Détermination automatique du centrage de la carte
        bbox = calculate_bounding_box(geojson_data.get("features", []))
        
        return {
            "status": "success",
            "layer_name": layer_name,
            "bounding_box": bbox,
            "center": [(bbox[1] + bbox[3]) / 2, (bbox[0] + bbox[2]) / 2], # Centrage automatique [Lat, Lon]
            "data": geojson_data
        }