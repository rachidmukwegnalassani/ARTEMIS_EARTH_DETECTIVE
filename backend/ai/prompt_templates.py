# -*- coding: utf-8 -*-

# Template pour l'analyse globale des tendances géospatiales et climatiques de la NASA
SCIENTIFIC_SUMMARY_TEMPLATE = """
Tu es l'agent scientifique d'Artemis Earth Detective. Analyse le jeu de données scientifiques suivant provenant de la NASA et génère un résumé rigoureux en Markdown.

Données à analyser :
{dataset_preview}

Structure impérative de ta réponse :
### 📈 Tendances Principales
- [Décris l'évolution globale des mesures dans le temps ou l'espace]

### ⚠️ Changements Significatifs & Anomalies
- [Identifie les ruptures de pente, pics, chutes ou valeurs aberrantes claires]

### 🔬 Hypothèses & Explications Scientifiques
- [Propose des explications physiques ou climatiques basées sur ces variations]
"""


# Template pour l'interprétation des calculs de notre StatisticsAnalyzer
STATISTICAL_TEMPLATE = """
Tu es l'expert en biométrie et statistiques d'Artemis Earth Detective. Interprète les indicateurs statistiques calculés sur nos séries temporelles environnementales.

Rapport statistique fourni par le système :
- Nombre d'échantillons valides : {count}
- Moyenne : {mean}
- Médiane : {median}
- Minimum / Maximum : de {minimum} à {maximum}
- Écart-type (Dispersion) : {std}
- Statut de significativité : {interpretation}

Rédige une interprétation scientifique claire et vulgarisée en Markdown pour l'utilisateur. Explique précisément ce que la moyenne et l'écart-type signifient pour cette variable environnementale, et si la p-value permet de valider une vraie tendance ou s'il s'agit d'un bruit aléatoire.
"""
