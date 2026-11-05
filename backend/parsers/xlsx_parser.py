# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, Any


class XlsxParser:

    @staticmethod
    def parse_sheets(file_path: str) -> dict:
        """Lit un fichier Excel et extrait les données de la première feuille."""
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            return {
                "status": "success",
                "total_records": len(df),
                "columns": list(df.columns),
                "data": df.to_dict(orient="records")
            }
        except Exception as e:
            return {"status": "error", "message": f"Échec de l'analyse Excel Pandas : {str(e)}"}
