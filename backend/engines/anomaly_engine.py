class AnomalyEngine:
    @staticmethod
    def scan_anomalies(records: list, threshold: float) -> list:
        """Détecte les écarts thermiques ou environnementaux qui dépassent la limite"""
        anomalies = []
        for idx, item in enumerate(records):
            val = item.get("value", 0.0)
            if abs(val) > threshold:
                anomalies.append({"index": idx, "value": val, "tag": "Critique"})
        return anomalies