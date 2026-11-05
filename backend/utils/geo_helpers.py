# -*- coding: utf-8 -*-
# backend/utils/geo_helpers.py

from typing import Dict, Any, Tuple, List


def validate_geojson(geojson_data: Dict[str, Any]) -> bool:
    """
    Vérifie si le fichier GeoJSON fourni respecte la structure standard 
    pour éviter les plantages du frontend ou du moteur spatial.
    """
    if not isinstance(geojson_data, dict):
        return False
    if "type" not in geojson_data:
        return False
    if geojson_data["type"] not in ["Feature", "FeatureCollection", "GeometryCollection", "Point", "Polygon"]:
        return False
    return True


def calculate_bounding_box(coordinates: List[Any]) -> Tuple[float, float, float, float]:
    """
    Calcule la boîte englobante (Bounding Box : min_lon, min_lat, max_lon, max_lat)
    à partir d'une liste de coordonnées pour recentrer automatiquement la carte.
    """
    lons = []
    lats = []
    
    def extract_coords(coords):
        if isinstance(coords, list) and len(coords) == 2 and isinstance(coords[0], (int, float)):
            lons.append(float(coords[0]))
            lats.append(float(coords[1]))
        elif isinstance(coords, list):
            for item in coords:
                extract_coords(item)

    extract_coords(coordinates)
    
    if not lons or not lats:
        return (0.0, 0.0, 0.0, 0.0)
        
    return (min(lons), min(lats), max(lons), max(lats))


def format_coordinates_for_display(lat: float, lon: float) -> str:
    """Formate proprement les coordonnées pour l'affichage textuel dans l'UI ou le chat."""
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "O"
    return f"{abs(lat):.4f}° {ns}, {abs(lon):.4f}° {ew}"
