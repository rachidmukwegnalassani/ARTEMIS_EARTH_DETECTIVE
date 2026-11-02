class TrendEngine:
    @staticmethod
    def calculate_trend(values: list) -> dict:
        """Analyse l'évolution d'une suite de valeurs pour en dégager la tendance générale"""
        if not values or len(values) < 2:
            return {"direction": "Stable", "rate": 0.0}
        
        first, last = values[0], values[-1]
        rate = ((last - first) / first) * 100 if first != 0 else 0.0
        
        if rate > 0.5:
            direction = "Hausse"
        elif rate < -0.5:
            direction = "Baisse"
        else:
            direction = "Stable"
            
        return {"direction": direction, "rate": round(rate, 2)}