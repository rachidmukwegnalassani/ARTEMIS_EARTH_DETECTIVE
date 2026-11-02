import json

class GeoJsonParser:
    @staticmethod
    def parse_file(file_path: str) -> dict:
        """Lit un fichier GeoJSON réel et extrait ses géométries et propriétés"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            features = data.get("features", [])
            extracted_features = []
            
            for feature in features:
                geometry = feature.get("geometry", {})
                properties = feature.get("properties", {})
                extracted_features.append({
                    "type": geometry.get("type"),
                    "coordinates": geometry.get("coordinates"),
                    "attributes": properties
                })
                
            return {
                "status": "success",
                "total_features": len(features),
                "features": extracted_features
            }
        except Exception as e:
            return {"status": "error", "message": f"Erreur de lecture GeoJSON : {str(e)}"}