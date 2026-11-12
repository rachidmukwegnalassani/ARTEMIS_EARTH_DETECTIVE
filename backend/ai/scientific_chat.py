# -*- coding: utf-8 -*-

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from backend.ai.context_manager import ContextManager
from backend.ai.file_analyzer import FileAnalyzer
from backend.ai.statistics_analyzer import StatisticsAnalyzer


class ScientificChat:

    def __init__(self):
        self.context = ContextManager()

    def _extract_real_values(self, filepath: Path) -> tuple[list[float], str]:
        ext = filepath.suffix.lower()

        if ext == ".csv":
            df = pd.read_csv(filepath, comment="#")
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
            raise ValueError(f"Extraction directe non prise en charge pour le format {ext}.")

        numeric_df = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
        ignore_cols = {"lat", "latitude", "lon", "longitude", "year", "month", "day", "doy", "id"}
        valid_cols = [c for c in numeric_df.columns if str(c).lower() not in ignore_cols]

        if not valid_cols:
            valid_cols = list(numeric_df.columns)
        if not valid_cols:
            raise ValueError("Aucune colonne numérique exploitable trouvée dans ce fichier.")

        target_col = valid_cols[0]
        values = numeric_df[target_col].dropna().astype(float).tolist()
        if len(values) < 3:
            raise ValueError("Le fichier doit contenir au moins 3 mesures pour évaluer une tendance.")

        return values, str(target_col)

    def _compute_real_significance(self, values: list[float]) -> dict:
        x = np.arange(len(values))
        y = np.array(values, dtype=float)
        slope, _, r_value, p_value, _ = scipy_stats.linregress(x, y)

        direction = "en hausse" if slope > 0 else "en baisse" if slope < 0 else "stable"
        is_significant = bool(p_value < 0.05)
        delta_total = float(y[-1] - y[0])

        verdict = (
            f"Changement SCIENTIFIQUEMENT SIGNIFICATIF (p = {p_value:.4f} < 0.05). "
            f"La variable évolue {direction} avec une variation nette de {delta_total:+.2f}."
            if is_significant
            else f"Variation NON SIGNIFICATIVE sur le plan statistique (p = {p_value:.4f} >= 0.05). "
            f"Les fluctuations observées ({delta_total:+.2f}) restent dans la variabilité naturelle."
        )

        return {
            "p_value": float(p_value),
            "slope": float(slope),
            "r_squared": float(r_value ** 2),
            "direction": direction,
            "is_significant": is_significant,
            "delta_total": delta_total,
            "interpretation": verdict
        }

    def analyze_file(self, filepath_str: str) -> dict:
        filepath = Path(filepath_str)
        if not filepath.exists():
            raise FileNotFoundError(f"Fichier introuvable : {filepath.name}")

        file_format = FileAnalyzer.detect_format(filepath.name)
        extracted_values, variable_name = self._extract_real_values(filepath)

        base_stats = StatisticsAnalyzer.compute(extracted_values)
        signif_stats = self._compute_real_significance(extracted_values)

        self.context.current_statistics = {**base_stats, **signif_stats}
        self.context.current_file = filepath.name
        self.context.current_variable = variable_name

        return {
            "filename": filepath.name,
            "format": file_format,
            "variable": variable_name,
            "statistics": self.context.current_statistics,
            "status": "Analyse scientifique complète"
        }

    def answer_question(self, question: str) -> str:
        clean_q = question.strip().lower()
        salutations = ("bonjour", "bonsoir", "salut", "hello", "hi", "coucou")

        if any(clean_q.startswith(mot) for mot in salutations):
            return (
                "Bonjour ! Je suis Artemis IA, votre détective du système Terre de la NASA. "
                "Importez un fichier réel (.csv, .xlsx, .geojson, .json) pour que j'analyse "
                "l'évolution des variables et vérifie si les changements sont scientifiquement significatifs."
            )

        stats = getattr(self.context, "current_statistics", None)
        filename = getattr(self.context, "current_file", None)
        variable = getattr(self.context, "current_variable", "la variable étudiée")

        if not stats or "mean" not in stats:
            return (
                "Aucun jeu de données NASA n'est encore chargé. Veuillez importer un fichier "
                "pour que je calcule ses tendances et sa significativité statistique."
            )

        if "significatif" in clean_q or "tendance" in clean_q or "évolution" in clean_q or "change" in clean_q:
            return f"Diagnostic sur '{filename}' (variable '{variable}') : {stats['interpretation']}"

        if "moyenne" in clean_q:
            return f"La moyenne calculée pour '{variable}' dans '{filename}' est de {stats['mean']:.2f} (médiane : {stats['median']:.2f})."

        return (
            f"Rapport complet sur '{filename}' — Variable '{variable}' ({stats['count']} observations) :\n"
            f"• Moyenne : {stats['mean']:.2f} | Min : {stats['minimum']:.2f} | Max : {stats['maximum']:.2f}\n"
            f"• Direction : Tendance {stats['direction']} ({stats['delta_total']:+.2f})\n"
            f"• Significativité : {stats['interpretation']}"
        )