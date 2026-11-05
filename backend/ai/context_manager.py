# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional, List


class ContextManager:

    def __init__(self):
        """
        Initialise le gestionnaire d'état contextuel pour Artemis Earth Detective.
        Garantit qu'aucune variable n'est indéfinie pour éviter les crashs de l'IA.
        """
        self.current_environment: Optional[str] = None   # Ex: "Marine", "Atmospheric", "Terrestrial"
        self.current_variable: Optional[str] = None      # Ex: "Sea Surface Temperature", "CO2"
        self.current_period: Optional[str] = None        # Ex: "2010-2025"
        self.current_dataset: Optional[str] = None       # Ex: "MODIS_SST_L3"
        
        # Structures de données complexes issues de nos analyseurs
        self.current_statistics: Dict[str, Any] = {}     # Données issues de StatisticsAnalyzer
        self.current_charts: List[Dict[str, Any]] = []    # Métadonnées des graphiques générés
        self.current_map: Dict[str, Any] = {}           # Données GeoJSON de SpatialAnalyzer

    def update_context(self, data: Dict[str, Any]) -> None:
        """
        Met à jour dynamiquement les variables de contexte avec les nouvelles données reçues.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def reset_context(self) -> None:
        """
        Réinitialise le contexte à zéro lorsque l'utilisateur change d'enquête ou de fichier.
        """
        self.current_environment = None
        self.current_variable = None
        self.current_period = None
        self.current_dataset = None
        self.current_statistics = {}
        self.current_charts = []
        self.current_map = {}
