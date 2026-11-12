import numpy as np

def compute_basic_stats(values: list[float]) -> dict:
    arr = np.array(values, dtype=float)
    return {
        "mean": float(np.mean(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "std": float(np.std(arr))
    }

def test_nasa_variable_statistics():
    sample_temperatures = [26.5, 27.0, 28.2, 26.8]
    stats = compute_basic_stats(sample_temperatures)
    assert round(stats["mean"], 2) == 27.12
    assert stats["min"] == 26.5
    assert stats["max"] == 28.2