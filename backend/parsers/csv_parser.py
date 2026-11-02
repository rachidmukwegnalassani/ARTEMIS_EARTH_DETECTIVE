import csv

class CsvParser:
    @staticmethod
    def parse_to_dict(file_path: str) -> dict:
        """Transforme un fichier CSV de données NASA en dictionnaire utilisable par l'API"""
        try:
            records = []
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(dict(row))
            return {
                "status": "success",
                "total_records": len(records),
                "data": records
            }
        except Exception as e:
            return {"status": "error", "message": f"Erreur de lecture CSV : {str(e)}"}