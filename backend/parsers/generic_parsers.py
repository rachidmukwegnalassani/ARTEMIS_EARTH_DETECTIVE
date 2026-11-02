import os

class GenericParser:
    @staticmethod
    def inspect_file(file_path: str) -> dict:
        """Détermine le format et extrait les métadonnées de base d'un fichier de production"""
        if not os.path.exists(file_path):
            return {"status": "error", "message": "Fichier introuvable sur le disque"}
        
        ext = os.path.splitext(file_path)[1].lower()
        return {
            "status": "success",
            "filename": os.path.basename(file_path),
            "extension": ext,
            "size_bytes": os.path.getsize(file_path)
        }