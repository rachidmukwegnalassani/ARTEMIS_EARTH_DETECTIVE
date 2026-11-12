import pandas as pd

def validate_dataset_structure(df: pd.DataFrame) -> bool:
    return not df.empty and len(df.columns) > 0

def test_dataset_validation():
    valid_df = pd.DataFrame({"latitude": [0.39], "longitude": [9.45], "value": [31.4]})
    empty_df = pd.DataFrame()
    assert validate_dataset_structure(valid_df) is True
    assert validate_dataset_structure(empty_df) is False