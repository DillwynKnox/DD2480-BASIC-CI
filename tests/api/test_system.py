from fastapi.testclient import TestClient

from basic_ci.main import app

client = TestClient(app)

def test_get_health():
    """
    test the /health endpoint
    """
    response = client.get("/health")
    assert response.status_code == 200, "/health should return code 200"
    assert response.json() == {"status": "ok"},"/health should tell status ok"

def test_get_version():
    """
    Docstring for test_get_version
    """
    response = client.get("/version")
    assert response.status_code == 200, "/version should return code 200"
    json_response = response.json()
    assert "version" in json_response, "/version response should contain 'version' key"
    assert isinstance(json_response["version"], str), "/version value should be a string"