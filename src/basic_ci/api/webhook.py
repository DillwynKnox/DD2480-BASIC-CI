from fastapi import APIRouter
from fastapi.params import Header

from basic_ci.schemes.push_payload import Push_payload

router = APIRouter(tags=["webhook"])

@router.post("/webhook")
def handle_webhook(
            payload: dict,
            x_hub_signature_256: str | None = Header(None)
        ) -> dict[str, str]:
    """Handle incoming github webhook payloads."""
    push_payload = Push_payload.model_validate(payload)
    print(push_payload)
    return {"status": "received"}