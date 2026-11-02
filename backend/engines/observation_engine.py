class ObservationEngine:
    @staticmethod
    def capture_observation(data: dict) -> dict:
        """Enregistre et qualifie une observation scientifique issue des capteurs"""
        return {
            "status": "observed",
            "metadata": data.get("metadata", {}),
            "measurements": data.get("values", [])
        }