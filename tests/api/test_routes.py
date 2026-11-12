from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code in [200, 404]

def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200