class ChangeEngine:
    @staticmethod
    def detect_absolute_change(old_value: float, new_value: float) -> dict:
        """Calcule la différence absolue entre deux relevés successifs d'une variable"""
        diff = new_value - old_value
        return {
            "previous": old_value,
            "current": new_value,
            "absolute_difference": round(diff, 4),
            "has_changed": diff != 0.0
        }