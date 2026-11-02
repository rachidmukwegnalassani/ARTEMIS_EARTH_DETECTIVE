class MissionsCatalog:
    def __init__(self):
        self.missions = {
            "landsat": {
                "fullname": "Landsat 8/9",
                "agency": "NASA / USGS",
                "data_type": "Images multispectrales / Réflectance de surface"
            },
            "aqua_terra": {
                "fullname": "MODIS (Satellites Aqua & Terra)",
                "agency": "NASA",
                "data_type": "Anomalies thermiques et couverture végétale"
            }
        }

    def list_active_missions(self) -> dict:
        return self.missions