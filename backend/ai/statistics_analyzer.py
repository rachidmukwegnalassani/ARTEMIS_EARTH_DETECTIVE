# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from typing import Union, List, Dict, Any


class StatisticsAnalyzer:

    @staticmethod
    def compute(values: Union[List[Union[int, float]], np.ndarray, pd.Series]) -> Dict[str, Any]:
        """
        Analyse les données de tendances de la NASA pour le module Artemis Earth Detective.
        Nettoie les données et extrait les statistiques descriptives au format standard.
        """
        # Conversion forcée en Série Pandas pour gérer efficacement les colonnes de fichiers de la NASA
        series = pd.Series(values)
        
        # Nettoyage automatique des valeurs manquantes (NaN) pour éviter le crash du backend FastAPI
        series_cleaned = series.dropna()

        # Sécurité si le fichier ou la colonne analysée ne contient aucune donnée valide
        if series_cleaned.empty:
            return {
                "count": 0,
                "mean": 0.0,
                "median": 0.0,
                "minimum": 0.0,
                "maximum": 0.0,
                "std": 0.0,
                "status": "No valid data to analyze"
            }

        # Calculs sécurisés convertis en types Python natifs (indispensable pour la sérialisation FastAPI/JSON)
        return {
            "count": int(series_cleaned.count()),
            "mean": float(series_cleaned.mean()),
            "median": float(series_cleaned.median()),
            "minimum": float(series_cleaned.min()),
            "maximum": float(series_cleaned.max()),
            "std": float(series_cleaned.std(ddof=0))  # ddof=0 pour garder la cohérence avec le calcul standard
        }

    @staticmethod
    def significance(p_value: float) -> Dict[str, Any]:
        """
        Évalue le seuil de significativité statistique (alpha = 0.05) pour les tendances détectées.
        Renvoie un dictionnaire structuré exploitable directement par le Chat IA d'Artemis.
        """
        try:
            p_val_float = float(p_value)
        except (ValueError, TypeError):
            return {"is_significant": False, "p_value": None, "interpretation": "Valeur p-value invalide."}

        is_significant = p_val_float < 0.05
        
        # Interprétation textuelle générée pour être directement lue par notre Chat IA
        if is_significant:
            interpretation = f"La tendance observée est statistiquement significative (p = {p_val_float:.4f}). Il y a moins de 5% de chances que ce résultat soit dû au hasard."
        else:
            interpretation = f"La tendance observée n'est pas statistiquement significative (p = {p_val_float:.4f}). Les variations peuvent être dues à des fluctuations aléatoires."

        return {
            "is_significant": is_significant,
            "p_value": p_val_float,
            "interpretation": interpretation
        }
