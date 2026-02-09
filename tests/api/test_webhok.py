import json
from pathlib import Path
from unittest.mock import MagicMock

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from basic_ci.core.signature import InvalidSignature, get_signature_verifier
from basic_ci.main import app

client = TestClient(app)

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


import json
from pathlib import Path
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from basic_ci.core.signature import get_signature_verifier
from basic_ci.main import app

client = TestClient(app)

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def test_handle_webhook_invalid_signature():
    """
    The webhook should return 403 if the signature verifier fails.
    """
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
    mock_verifier_instance = MagicMock()
    app.dependency_overrides[get_signature_verifier] = lambda: mock_verifier_instance

    payload = load_json("webhook.json")
    dummy_signature = "sha256=valid_signature"
    
    response = client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": dummy_signature},
    )

    assert response.status_code == 200, "Valid signature should return 200"

    app.dependency_overrides.clear()

def test_handle_webhook_invalid_payload():
    """An invalid payload should return 422."""
    payload = {"invalid": "data"}
    mock_verifier_instance = MagicMock()

    app.dependency_overrides[get_signature_verifier] = lambda: mock_verifier_instance
    with pytest.raises(ValidationError):
        response = client.post(
            "/webhook",
            json=payload,
            headers={"X-Hub-Signature-256": "sha256=valid_signature"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 403, "Invalid Signature should return 403"


def test_handle_valid_webhook_with_valid_signature():
    """A valid signature should allow the webhook to be processed."""
    mock_verifier_instance = MagicMock()
    
    app.dependency_overrides[get_signature_verifier] = lambda: mock_verifier_instance

    payload = load_json("webhook.json")
    dummy_signature = "sha256=valid_signature"
    
    response = client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": dummy_signature},
    )

    assert response.status_code == 200, "Valid signature should return 200"

    app.dependency_overrides.clear()

def test_handle_webhook_invalid_payload():
    """An invalid payload should return 422."""
    payload = {"invalid": "data"}
    mock_verifier_instance = MagicMock()

    app.dependency_overrides[get_signature_verifier] = lambda: mock_verifier_instance
    with pytest.raises(ValidationError):
        response = client.post(
            "/webhook",
            json=payload,
            headers={"X-Hub-Signature-256": "sha256=valid_signature"},
        )

    app.dependency_overrides.clear()