import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from basic_ci.core.signature import get_signature_verifier
from basic_ci.main import app
from basic_ci.services.task_service import get_TaskService

client = TestClient(app)

DATA_DIR = Path(__file__).parent.parent / "data"

def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    app.dependency_overrides.clear()

def test_handle_webhook_invalid_signature():
    """The webhook should return 403 if the signature verifier fails."""
    def mock_get_signature_verifier_fail():
        raise HTTPException(status_code=403, detail="Signature mismatch")
    
    app.dependency_overrides[get_signature_verifier] = mock_get_signature_verifier_fail

    payload = load_json("webhook.json")
    
    response = client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": "sha256=invalid_signature"},
    )

    assert response.status_code == 403

def test_handle_valid_webhook_with_valid_signature():
    """A valid signature should allow the webhook to be processed."""
    mock_verifier = MagicMock()
    mock_service = MagicMock()
    
    # Return a dictionary that satisfies the TaskResult Pydantic model
    mock_service.run_task.return_value = {
        "run_id": "test-123",
        "repo_url": "https://github.com/user/repo",
        "branch": "main",
        "commit_sha": "abc12345",
        "status": "success"
    }

    app.dependency_overrides[get_signature_verifier] = lambda: mock_verifier
    app.dependency_overrides[get_TaskService] = lambda: mock_service

    payload = load_json("webhook.json")
    
    response = client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": "sha256=valid_signature"},
    )

    assert response.status_code == 200

def test_handle_webhook_invalid_payload():
    """An invalid payload should return 422 Unprocessable Entity."""
    app.dependency_overrides[get_signature_verifier] = lambda: MagicMock()
    
    payload = {"invalid": "data"}
    
    response = client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": "sha256=valid_signature"},
    )

    assert response.status_code == 422