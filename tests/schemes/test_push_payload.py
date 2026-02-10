
import json

from basic_ci.schemes.push_payload import Push_payload


def test_push_payload_scheme():
    with open("tests/data/webhook.json","r") as f:
        payload = json.load(f)
    push_payload = Push_payload.model_validate(payload)