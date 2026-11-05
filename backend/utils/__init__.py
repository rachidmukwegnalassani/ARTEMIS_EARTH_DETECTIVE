# -*- coding: utf-8 -*-

# Ce fichier expose proprement tous nos utilitaires de support pour qu'ils soient 
# accessibles directement depuis n'importe quel autre endroit du projet.

from backend.utils.geo_helpers import (
    validate_geojson, 
    calculate_bounding_box, 
    format_coordinates_for_display
)
from backend.utils.time_helpers import (
    filter_time_series_by_range, 
    format_timestamp_for_ui, 
    aggregate_data_by_period
)
from backend.utils.parsers import (
    format_ui_table_for_llm,
    parse_nasa_text_document
)

# La variable __all__ indique à VS Code que ces fonctions sont exportées.
# Cela supprime l'affichage grisé inutile.
__all__ = [
    "validate_geojson",
    "calculate_bounding_box",
    "format_coordinates_for_display",
    "filter_time_series_by_range",
    "format_timestamp_for_ui",
    "aggregate_data_by_period",
    "format_ui_table_for_llm",
    "parse_nasa_text_document"
]
