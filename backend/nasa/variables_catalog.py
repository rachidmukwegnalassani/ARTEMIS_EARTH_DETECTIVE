class VariablesCatalog:
    def __init__(self):
        # Liste des variables clés de la NASA à suivre pour le projet
        self.catalog = {
            "surface_temp": {
                "name": "Température de surface de la Terre",
                "unit": "°C",
                "critical_threshold": 35.0
            },
            "soil_moisture": {
                "name": "Humidité des sols",
                "unit": "m3/m3",
                "critical_threshold": 0.15
            },
            "carbon_monoxide": {
                "name": "Monoxyde de carbone atmosphérique",
                "unit": "ppb",
                "critical_threshold": 150.0
            }
        }

    def get_all_variables(self) -> dict:
        return self.catalog

    def get_variable_details(self, variable_id: str) -> dict:
        return self.catalog.get(variable_id, {"error": "Variable non répertoriée"})