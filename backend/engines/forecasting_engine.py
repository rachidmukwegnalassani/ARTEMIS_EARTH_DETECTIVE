class ForecastingEngine:
    @staticmethod
    def predict_next(values: list) -> float:
        """Calcule une projection linéaire simple pour estimer le prochain point de donnée"""
        if not values:
            return 0.0
        if len(values) == 1:
            return values[0]
        
        # Moyenne des derniers écarts pour projeter la suite
        diffs = [values[i] - values[i-1] for i in range(1, len(values))]
        avg_diff = sum(diffs) / len(diffs)
        return round(values[-1] + avg_diff, 2)