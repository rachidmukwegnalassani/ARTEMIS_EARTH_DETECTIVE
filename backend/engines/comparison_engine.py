class ComparisonEngine:
    @staticmethod
    def compare_datasets(dataset_a: list, dataset_b: list) -> dict:
        """Compare la moyenne de deux ensembles de données pour en sortir les écarts"""
        avg_a = sum(dataset_a) / len(dataset_a) if dataset_a else 0.0
        avg_b = sum(dataset_b) / len(dataset_b) if dataset_b else 0.0
        
        return {
            "average_a": round(avg_a, 2),
            "average_b": round(avg_b, 2),
            "ratio": round(avg_a / avg_b, 2) if avg_b != 0.0 else 0.0
        }