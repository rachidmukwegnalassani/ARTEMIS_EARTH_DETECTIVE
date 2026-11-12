# -*- coding: utf-8 -*-

import json
from pathlib import Path
import pandas as pd
from backend.ai.context_manager import ContextManager
from backend.ai.file_analyzer import FileAnalyzer
from backend.ai.statistics_analyzer import StatisticsAnalyzer


class ScientificChat:

    def __init__(self):
        self.context = ContextManager()

    def _extract_real_values(self, filepath: Path) -> tuple[list[float], str]:
        ext = filepath.suffix.lower()

        if ext == ".csv":
            df = pd.read_csv(filepath)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(filepath)
        elif ext in (".json", ".geojson"):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "features" in data:
                records = [feat.get("properties", {}) for feat in data["features"]]
                df = pd.DataFrame(records)
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.json_normalize(data)
        else:
            raise ValueError(f"Extraction numérique directe non prise en charge pour le format {ext}.")

        numeric_df = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
        if numeric_df.empty:
            raise ValueError("Aucune colonne numérique exploitable n'a été trouvée dans ce fichier.")

        target_col = numeric_df.columns[0]
        values = numeric_df[target_col].dropna().astype(float).tolist()
        if not values:
            raise ValueError(f"La colonne '{target_col}' ne contient aucune valeur valide.")

        return values, str(target_col)

    def analyze_file(self, filepath_str: str) -> dict:
        filepath = Path(filepath_str)
        if not filepath.exists():
            raise FileNotFoundError(f"Le fichier introuvable : {filepath.name}")

        file_format = FileAnalyzer.detect_format(filepath.name)
        extracted_values, variable_name = self._extract_real_values(filepath)

        stats = StatisticsAnalyzer.compute(extracted_values)
        signif = StatisticsAnalyzer.significance(p_value=0.05)

        self.context.current_statistics = {**stats, **signif}
        self.context.current_file = filepath.name
        self.context.current_variable = variable_name

        return {
            "filename": filepath.name,
            "format": file_format,
            "variable": variable_name,
            "statistics": self.context.current_statistics,
            "status": "Analyse réelle terminée"
        }

    def answer_question(self, question: str) -> str:
        clean_q = question.strip().lower()
        salutations = ("bonjour", "bonsoir", "salut", "hello", "hi", "coucou")

        if any(clean_q.startswith(mot) for mot in salutations):
            return (
                "Bonjour ! Je suis Artemis IA, votre assistant d'analyse des données de la NASA. "
                "Je suis actif. Importez un fichier réel (.csv, .xlsx, .geojson, .json) pour que j'en extraie "
                "les statistiques et réponde à vos questions."
            )

        stats = getattr(self.context, "current_statistics", None)
        filename = getattr(self.context, "current_file", None)
        variable = getattr(self.context, "current_variable", "la variable étudiée")

        if not stats or "mean" not in stats:
            return (
                "Aucun fichier de données n'a encore été analysé. "
                "Veuillez charger un jeu de données réel depuis le panneau de gauche."
            )

        if "moyenne" in clean_q:
            return f"Pour '{filename}' (variable : {variable}), la moyenne réelle calculée est de {stats['mean']:.2f}."
        if "minimum" in clean_q or "min" in clean_q:
            return f"La valeur minimale observée sur '{variable}' dans '{filename}' est de {stats['minimum']:.2f}."
        if "maximum" in clean_q or "max" in clean_q:
            return f"La valeur maximale observée sur '{variable}' dans '{filename}' est de {stats['maximum']:.2f}."

        return (
            f"Synthèse réelle sur '{filename}' (variable : {variable}, {stats['count']} mesures) : "
            f"Moyenne = {stats['mean']:.2f}, Médiane = {stats['median']:.2f}, "
            f"Min = {stats['minimum']:.2f}, Max = {stats['maximum']:.2f}, Écart-type = {stats['std']:.2f}. "
            f"{stats['interpretation']}"
        )