# -*- coding: utf-8 -*-

import pandas as pd
from typing import Dict, Any


class CsvParser:

    @staticmethod
    def parse_to_dict(file_path: str) -> dict:
        """Lit un fichier CSV de la NASA de manière ultra-rapide avec Pandas."""
        try:
            df = pd.read_csv(file_path)
            records = df.to_dict(orient="records")
            return {
                "status": "success",
                "total_records": len(df),
                "columns": list(df.columns),
                "data": records
            }
        except Exception as e:
            return {"status": "error", "message": f"Échec de l'analyse CSV Pandas : {str(e)}"}
