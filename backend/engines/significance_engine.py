class SignificanceEngine:
    @staticmethod
    def evaluate_significance(change_rate: float, threshold: float = 5.0) -> dict:
        """Détermine si le taux de changement mesuré est critique ou statistiquement significatif"""
        is_significant = abs(change_rate) >= threshold
        return {
            "change_rate_percentage": round(change_rate, 2),
            "threshold_applied": threshold,
            "is_significant": is_significant,
            "priority_level": "HAUTE" if is_significant else "NORMALE"
        }