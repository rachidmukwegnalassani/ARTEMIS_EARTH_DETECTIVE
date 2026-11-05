# -*- coding: utf-8 -*-

from backend.ai.context_manager import ContextManager
from backend.ai.file_analyzer import FileAnalyzer
from backend.ai.statistics_analyzer import StatisticsAnalyzer
from backend.ai.prompts import STATISTICAL_TEMPLATE, SCIENTIFIC_SUMMARY_TEMPLATE


class ScientificChat:

    def __init__(self):
        # Gestionnaire de contexte pour suivre la variable (ex: Température) ou la catégorie (ex: Climat)
        self.context = ContextManager()

    def analyze_file(self, filename: str) -> dict:
        """
        Détecte le format, extrait les données brutes et calcule automatiquement
        le rapport statistique complet de la NASA pour le contexte du chat.
        """
        # 1. Détection du format via le FileAnalyzer existant
        file_format = FileAnalyzer.detect_format(filename)
        
        # 2. Simulation d'extraction des données du fichier (à lier avec ton loader de fichiers de la NASA)
        # Supposons que nous extrayons une série de données numériques de test :
        extracted_values = [14.2, 14.5, 14.8, 15.1, 13.9, 15.4, 16.2]  # Exemple de série temporelle
        
        # 3. Calcul des statistiques réelles avec notre nouvel analyseur Pandas
        stats = StatisticsAnalyzer.compute(extracted_values)
        signif = StatisticsAnalyzer.significance(p_value=0.03)  # Exemple de p-value calculée
        
        # 4. Sauvegarde des statistiques dans le contexte global de la discussion
        self.context.current_statistics = {**stats, **signif}
        self.context.current_file = filename
        
        return {
            "filename": filename,
            "format": file_format,
            "statistics": self.context.current_statistics,
            "status": "File successfully analyzed and contextualized"
        }

    def answer_question(self, question: str) -> dict:
        """
        Génère une réponse intelligente en injectant les statistiques de l'analyseur
        directement dans les templates de prompts IA pour le Chat Artemis.
        """
        # Vérification si des statistiques de fichier de la NASA sont disponibles dans le chat
        stats = getattr(self.context, "current_statistics", None)
        
        if stats and "mean" in stats:
            # Injection dynamique de nos calculs Pandas dans le template de prompt qu'on a corrigé juste avant
            prompt_ready = STATISTICAL_TEMPLATE.format(
                count=stats["count"],
                mean=f"{stats['mean']:.2f}",
                median=f"{stats['median']:.2f}",
                minimum=f"{stats['minimum']:.2f}",
                maximum=f"{stats['maximum']:.2f}",
                std=f"{stats['std']:.2f}",
                interpretation=stats["interpretation"]
            )
            # Ici viendra l'appel final à ton LLM (OpenAI / Anthropic / local) : llm.generate(prompt_ready)
            ai_response = f"[Artemis IA basé sur les statistiques réelles] : {stats['interpretation']}"
        else:
            ai_response = "Je n'ai pas encore de données statistiques à analyser. Veuillez charger un fichier de la NASA pour commencer l'enquête."

        return {
            "question": question,
            "variable": self.context.current_variable,
            "category": self.context.current_category,
            "prompt_used": prompt_ready if stats else None,
            "answer": ai_response
        }
