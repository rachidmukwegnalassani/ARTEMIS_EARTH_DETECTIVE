# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional


class ExplanationEngine:

    @staticmethod
    def explain_trend(trend: float, variable_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyse l'intensité d'une tendance numérique et génère une explication
        scientifique qualifiée et vulgarisée pour le Chat d'Artemis.
        """
        try:
            val_trend = float(trend)
        except (ValueError, TypeError):
            return {
                "intensity": "Inconnue",
                "explanation": "Impossible d'analyser la tendance : valeur numérique invalide.",
                "status": "error"
            }

        # Détermination de l'intensité de la tendance avec des seuils qualitatifs
        abs_trend = abs(val_trend)
        if abs_trend < 0.01:
            intensity = "stable"
        elif abs_trend < 0.05:
            intensity = "modérée"
        elif abs_trend < 0.15:
            intensity = "significative"
        else:
            intensity = "critique"

        # Dictionnaire de contextualisation pour adapter le vocabulaire scientifique
        var_lower = str(variable_name).lower() if variable_name else ""
        
        if "temp" in var_lower or "sst" in var_lower:
            verb_up, verb_down = "un réchauffement", "un refroidissement"
        elif "co2" in var_lower or "gas" in var_lower or "emissions" in var_lower:
            verb_up, verb_down = "une accumulation de gaz", "une baisse des concentrations"
        elif "forest" in var_lower or "tree" in var_lower or "ndvi" in var_lower:
            verb_up, verb_down = "une régénération de la végétation", "une déforestation / dégradation"
        elif "sea_level" in var_lower or "water" in var_lower:
            verb_up, verb_down = "une élévation du niveau des eaux", "une baisse du niveau des eaux"
        else:
            verb_up, verb_down = "une augmentation", "une diminution"

        # Génération de l'explication scientifique dynamique
        if intensity == "stable":
            explanation = f"La variable {variable_name or ''} montre une stabilité relative sur la période étudiée, sans fluctuation majeure."
        elif val_trend > 0:
            explanation = f"Les données indiquent {verb_up} avec une intensité {intensity} (facteur de tendance : +{val_trend:.4f})."
        else:
            explanation = f"Les données indiquent {verb_down} avec une intensité {intensity} (facteur de tendance : {val_trend:.4f})."

        return {
            "intensity": intensity,
            "direction": "up" if val_trend > 0 and intensity != "stable" else ("down" if val_trend < 0 and intensity != "stable" else "stable"),
            "explanation": explanation,
            "status": "success"
        }
