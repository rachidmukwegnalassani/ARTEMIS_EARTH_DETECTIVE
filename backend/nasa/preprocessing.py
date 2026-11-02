class DataPreprocessor:
    @staticmethod
    def clean_records(records: list, key_name: str, fill_value: float = 0.0) -> list:
        """
        Nettoie génériquement une liste de relevés scientifiques de la NASA.
        Élimine ou remplace les valeurs manquantes, vides ou aberrantes (NaN).
        """
        cleaned = []
        for record in records:
            new_rec = dict(record)
            val = new_rec.get(key_name)
            
            # Gestion des données vides ou invalides fréquemment reçues des API
            if val is None or val == "" or val == "NaN":
                new_rec[key_name] = fill_value
            else:
                try:
                    new_rec[key_name] = float(val)
                except ValueError:
                    new_rec[key_name] = fill_value
            cleaned.append(new_rec)
        return cleaned

    @staticmethod
    def filter_by_bounds(records: list, key_name: str, min_val: float, max_val: float) -> list:
        """
        Filtre les données pour ne garder que les valeurs comprises dans les seuils physiques.
        Utile pour éliminer les erreurs de capteurs satellites le jour de la compétition.
        """
        return [r for r in records if min_val <= r.get(key_name, 0.0) <= max_val]