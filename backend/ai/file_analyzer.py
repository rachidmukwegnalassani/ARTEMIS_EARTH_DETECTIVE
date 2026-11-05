# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union, Dict, Any


class FileAnalyzer:

    # Mapping étendu et documenté des formats de données de la NASA et géospatiales
    FORMAT_MAPPING: Dict[str, str] = {
        ".geojson": "geojson",
        ".shp": "shapefile",
        ".tif": "raster",
        ".tiff": "raster",
        ".csv": "table",
        ".xlsx": "excel",
        ".txt": "text",
        ".json": "json",
        ".pdf": "pdf",
        ".nc": "netcdf",    # Format standard de la NASA pour les données gridded (climat)
        ".hdf": "hdf",      # Hierarchical Data Format (satellites EarthData)
        ".h5": "hdf"        # Variante fréquente du format HDF5
    }

    @staticmethod
    def detect_format(file_input: Union[str, Path]) -> Dict[str, Any]:
        """
        Détecte le format d'un fichier scientifique ou géospatial.
        Valide l'extension et effectue des vérifications de cohérence de base.
        """
        # Conversion sécurisée en objet Path
        path_obj = Path(file_input)
        ext = path_obj.suffix.lower()
        
        detected_format = FileAnalyzer.FORMAT_MAPPING.get(ext, "unknown")

        # Métadonnées de base sur le fichier pour enrichir le contexte d'Artemis
        file_info = {
            "filename": path_obj.name,
            "extension": ext,
            "format": detected_format,
            "is_valid": detected_format != "unknown",
            "warning": None
        }

        # Alerte spécifique pour le format Shapefile (nécessite ses fichiers compagnons)
        if detected_format == "shapefile":
            file_info["warning"] = "Attention : Un fichier Shapefile requiert ses composants secondaires (.shx, .dbf, .prj) dans le même répertoire pour être lu correctement."

        return file_info
