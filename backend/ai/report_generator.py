# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional


class ReportGenerator:

    @staticmethod
    def generate_markdown(
        title: str,
        content: str,
        context_data: Optional[Dict[str, Any]] = None,
        timestamp_str: Optional[str] = None
    ) -> str:
        """
        Génère un rapport scientifique complet au format Markdown pour Artemis Earth Detective.
        Exclut totalement le module datetime brut au profit de chaînes de caractères ISO contrôlées.
        """
        # Gestion de la date de génération sans utiliser le module datetime déprécié
        generated_at = timestamp_str if timestamp_str else "Date de génération standardisée par le système"

        # Extraction des métadonnées du contexte si disponibles
        metadata_section = ""
        stats_section = ""
        
        if context_data:
            environment = context_data.get("current_environment", "Non spécifié")
            variable = context_data.get("current_variable", "Non spécifiée")
            period = context_data.get("current_period", "Non spécifiée")
            dataset = context_data.get("current_dataset", "Non spécifié")
            
            metadata_section = f"""###  Métadonnées de l'Enquête
- **Environnement d'étude :** {environment}
- **Variable observée :** {variable}
- **Période d'analyse :** {period}
- **Jeu de données NASA :** {dataset}
"""

            # Intégration optionnelle des indicateurs calculés par notre StatisticsAnalyzer
            stats = context_data.get("current_statistics", {})
            if stats and "mean" in stats:
                stats_section = f"""###  Indicateurs Statistiques Calculés
- **Échantillons valides :** {stats.get('count', 'N/A')}
- **Moyenne :** {stats.get('mean', 0.0):.4f}
- **Médiane :** {stats.get('median', 0.0):.4f}
- **Écart-type :** {stats.get('std', 0.0):.4f}
- **Significativité :** {stats.get('interpretation', 'Non évaluée')}
"""

        # Assemblage final du rapport Markdown structuré pour l'affichage ordinateur ou l'export PDF
        report_template = f"""#  RAPPORT D'ENQUÊTE ENVIRONNEMENTALE : {title.upper()}

**Module :** Artemis Earth Detective (NASA Space Apps Challenge)
**Généré le :** {generated_at}

---

{metadata_section}

{stats_section}

### Conclusions & Analyses Détaillées
{content}

---
*Fin du document officiel de l'analyseur Artemis.*
"""
        return report_template.strip()
