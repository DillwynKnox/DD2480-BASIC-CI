from fastapi import APIRouter

router = APIRouter(tags=["webhook"])

@router.post("/webhook")
def handle_webhook(payload: dict) -> dict[str, str]:
    """Handle incoming webhook payloads."""
    print("Received webhook payload:", payload)
    return {"status": "received"}