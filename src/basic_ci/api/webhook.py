from fastapi import APIRouter
from fastapi.params import Depends, Header

from basic_ci.core.signature import Signature_verifier, get_signature_verifier
from basic_ci.schemes.push_payload import Push_payload

router = APIRouter(tags=["webhook"])

@router.post("/webhook")
def handle_webhook(
            payload: dict,
            verifier: Signature_verifier = Depends(get_signature_verifier)
        ) -> dict[str, str]:
    """Verifyies Signature and extract payload from incoming github webhook payloads."""
    push_payload = Push_payload.model_validate(payload)
    print(push_payload)
    return {"status": "received"}