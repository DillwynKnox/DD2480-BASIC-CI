from fastapi.testclient import TestClient

from basic_ci.main import app

client = TestClient(app)

def test_get_root():
    """
    Test if the root returns the expected message.
    """
    response = client.get("/")
    assert response.status_code == 200, "Root endpoint did not return status code 200."
    assert response.json() == {"message": "Basic CI pipeline is running"}, "Root endpoint did not return the expected message."