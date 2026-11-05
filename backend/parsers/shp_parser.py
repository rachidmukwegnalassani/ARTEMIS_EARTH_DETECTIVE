# -*- coding: utf-8 -*-

import geopandas as gpd
from typing import Dict, Any


class ShpParser:

    @staticmethod
    def parse_shapefile(base_path: str) -> dict:
        """Analyse la structure et extrait les données d'un vrai fichier ESRI Shapefile."""
        try:
            gdf = gpd.read_file(base_path)
            bounds = gdf.total_bounds
            return {
                "status": "success",
                "total_features": len(gdf),
                "geometry_type": str(gdf.geom_type.iloc[0]) if not gdf.empty else "None",
                "bounding_box": {"xmin": float(bounds[0]), "ymin": float(bounds[1]), "xmax": float(bounds[2]), "ymax": float(bounds[3])},
                "crs": str(gdf.crs)
            }
        except Exception as e:
            return {"status": "error", "message": f"Erreur de traitement Shapefile GeoPandas : {str(e)}"}
