# -*- coding: utf-8 -*-

import re
from typing import List

class TextAnalyzer:

    def __init__(self, content: str):
        self.content = content

    def summarize(self) -> str:
        """Génère un résumé ou extrait les premières lignes du document joint."""
        if len(self.content) < 300:
            return self.content

        return self.content[:300] + "..."

    def extract_numbers(self) -> List[str]:
        """Extrait toutes les données numériques et décimales du texte."""
        return re.findall(
            r"\d+(?:\.\d+)?",
            self.content
        )

    def detect_keywords(self) -> List[str]:
        """Détecte les variables de la NASA présentes dans le texte."""
        keywords = [
            "temperature",
            "precipitation",
            "humidity",
            "ndvi",
            "vegetation",
            "flood",
            "drought",
            "sea level"
        ]

        return [
            keyword
            for keyword in keywords
            if keyword.lower() in self.content.lower()
        ]

    def generate_scientific_summary(self) -> str:
        """Génère une réponse d'analyse automatique pour le chat Artemis."""
        detected = self.detect_keywords()
        numbers = self.extract_numbers()
        
        if not detected:
            return "Le document analysé ne semble pas contenir de variables environnementales connues du système Artemis."
            
        return (
            f"Analyse textuelle terminée. Le document joint traite spécifiquement des thématiques suivantes : "
            f"{', '.join(detected)}. J'y ai détecté {len(numbers)} indicateurs numériques isolés. "
            f"Ces données sont prêtes à être croisées avec vos couches cartographiques."
        )