from fastapi import APIRouter

from basic_ci.schemes.push_payload import Push_payload

router = APIRouter(tags=["webhook"])

@router.post("/webhook")
def handle_webhook(payload: dict) -> dict[str, str]:
    """Handle incoming github webhook payloads."""
    print("Received webhook payload:", payload)
    push_payload = Push_payload.model_validate(payload)
    print("================")
    print(push_payload)
    return {"status": "received"}