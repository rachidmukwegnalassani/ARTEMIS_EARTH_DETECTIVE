# -*- coding: utf-8 -*-

import geopandas as gpd
import numpy as np
from typing import Dict, Any, Union
from pathlib import Path


class SpatialAnalyzer:

    @staticmethod
    def calculate_extent(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Calcule l'emprise géographique (Bounding Box) et la superficie totale 
        d'une couche vectorielle (GeoJSON / Shapefile) de la NASA.
        """
        try:
            path_obj = Path(file_path)
            if not path_obj.exists():
                return {"error": "Fichier introuvable pour le calcul de l'emprise."}

            # Lecture du fichier géospatial avec GeoPandas
            gdf = gpd.read_file(path_obj)

            if gdf.empty:
                return {"error": "Le fichier géospatial ne contient aucune entité."}

            # Extraction de la Bounding Box globale [xmin, ymin, xmax, ymax]
            bounds = gdf.total_bounds
            
            # Calcul de la superficie totale (si système de projection métrique, sinon approximation)
            # On s'assure d'avoir un type Python natif (float) pour éviter les crashs de sérialisation JSON
            total_area = float(gdf.geometry.area.sum())

            return {
                "bounding_box": {
                    "xmin": float(bounds[0]),
                    "ymin": float(bounds[1]),
                    "xmax": float(bounds[2]),
                    "ymax": float(bounds[3])
                },
                "total_entities": len(gdf),
                "calculated_area_sq_m": total_area,
                "crs": str(gdf.crs)
            }
        except Exception as e:
            return {"error": f"Erreur lors du calcul de l'emprise : {str(e)}"}

    @staticmethod
    def detect_changes(baseline_data: Union[list, np.ndarray], current_data: Union[list, np.ndarray]) -> Dict[str, Any]:
        """
        Détecte les changements environnementaux (ex: déforestation, fonte des glaces, recul des eaux)
        entre une situation de référence (baseline) et une situation actuelle.
        Fonctionne sur des matrices de pixels ou des séries géospatiales.
        """
        arr_base = np.array(baseline_data, dtype=float)
        arr_current = np.array(current_data, dtype=float)

        if arr_base.shape != arr_current.shape:
            return {"error": "Les dimensions des matrices géospatiales de comparaison doivent être identiques."}

        # Calcul de la différence brute absolue et relative
        diff = arr_current - arr_base
        mean_change = float(np.nanmean(diff))
        max_regression = float(np.nanmin(diff))
        max_progression = float(np.nanmax(diff))

        # Évaluation globale de la tendance environnementale
        if mean_change > 0.05:
            trend = "Augmentation / Progression globale de la variable détectée."
        elif mean_change < -0.05:
            trend = "Diminution / Régression globale de la variable détectée."
        else:
            trend = "Stabilité relative de la zone d'étude."

        return {
            "mean_change": mean_change,
            "max_regression": max_regression,
            "max_progression": max_progression,
            "environmental_trend": trend
        }

    @staticmethod
    def generate_layers(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Prépare et convertit une couche géospatiale brute au format GeoJSON standardisé
        et nettoyé, prêt à être consommé directement par la carte du frontend sur l'ordinateur.
        """
        try:
            path_obj = Path(file_path)
            gdf = gpd.read_file(path_obj)

            # Reprojection automatique en WGS84 (EPSG:4326) si nécessaire pour l'affichage web (Leaflet/Mapbox)
            if gdf.crs and str(gdf.crs) != "EPSG:4326":
                gdf = gdf.to_crs(epsg=4326)

            # Conversion en dictionnaire GeoJSON standard
            geojson_data = gdf.__geo_interface__

            return {
                "status": "success",
                "layer_type": "vector",
                "geojson": geojson_data
            }
        except Exception as e:
            return {"error": f"Erreur lors de la génération de la couche web : {str(e)}"}
