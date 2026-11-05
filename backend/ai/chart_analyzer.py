# -*- coding: utf-8 -*-

from typing import List, Dict, Any, Union

class ChartAnalyzer:

    @staticmethod
    def identify_trend(values: List[Union[int, float, str]]) -> str:
        """Identifie de manière sécurisée la tendance globale de la courbe graphique."""
        try:
            # Conversion propre en float pour éviter les plantages de types
            clean_values = [float(v) for v in values if v is not None]
        except (ValueError, TypeError):
            return "Format de données invalide"

        if len(clean_values) < 2:
            return "Données insuffisantes"

        if clean_values[-1] > clean_values[0]:
            return "En augmentation"

        if clean_values[-1] < clean_values[0]:
            return "En diminution"

        return "Stable"

    @staticmethod
    def detect_extremes(values: List[Union[int, float, str]]) -> Dict[str, Any]:
        """Extrait de manière sécurisée les valeurs minimales et maximales observées."""
        try:
            clean_values = [float(v) for v in values if v is not None]
        except (ValueError, TypeError):
            return {"min": "N/A", "max": "N/A"}

        if not clean_values:
            return {"min": "N/A", "max": "N/A"}

        return {
            "min": min(clean_values),
            "max": max(clean_values)
        }

    @staticmethod
    def generate_trend_report(variable_name: str, values: List[Any]) -> str:
        """Génère le texte scientifique pour le bloc Graphiques & modélisations."""
        trend = ChartAnalyzer.identify_trend(values)
        extremes = ChartAnalyzer.detect_extremes(values)
        
        if trend in ["Données insuffisantes", "Format de données invalide"]:
            return f"Analyse graphique interrompue : {trend} pour l'indicateur {variable_name}."
            
        return (
            f"Modélisation temporelle générée pour la courbe {variable_name}. "
            f"La tendance générale est qualifiée : '{trend}'. "
            f"Les valeurs critiques enregistrées oscillent entre un minimum de {extremes['min']} "
            f"et un maximum de {extremes['max']} sur la plage d'observation actuelle."
        )