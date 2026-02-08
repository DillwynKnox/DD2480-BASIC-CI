import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from basic_ci.main import app

client = TestClient(app)

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def test_handle_webhook_valid_payload():
    payload = load_json("webhook.json")

    response = client.post(
        "/webhook",
        json=payload,
        headers={
            "X-Hub-Signature-256": "sha256=dummy"
        },
    )

    assert response.status_code == 200
    assert response.json() == {"status": "received"}
