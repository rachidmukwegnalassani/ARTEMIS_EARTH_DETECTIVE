from pathlib import Path

SUPPORTED_FORMATS = {
    ".geojson", ".json", ".shp", ".tif", ".tiff",
    ".nc", ".hdf", ".csv", ".xlsx", ".txt", ".pdf"
}

def is_supported_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in SUPPORTED_FORMATS

def test_valid_nasa_extensions():
    assert is_supported_file("climate_data.nc") is True
    assert is_supported_file("libreville_zones.geojson") is True
    assert is_supported_file("statistics.csv") is True

def test_invalid_extensions():
    assert is_supported_file("malware.exe") is False
    assert is_supported_file("archive.zip") is False