from fastapi import APIRouter
from fastapi.params import Depends

from basic_ci.core.signature import Signature_verifier, get_signature_verifier
from basic_ci.schemes.push_payload import Push_payload
from basic_ci.services.task_service import TaskService, get_TaskService

router = APIRouter(tags=["webhook"])

@router.post("/webhook")
def handle_webhook(
            payload: dict,
            verifier: Signature_verifier = Depends(get_signature_verifier),
            task_service:TaskService = Depends(get_TaskService)
        ) -> dict[str, str]:
    """Verifyies Signature and extract payload from incoming github webhook payloads."""
    push_payload = Push_payload.model_validate(payload)
    print(f"Received webhook for repo: {push_payload.repo_url}, commit: {push_payload.commit_sha}")
    result = task_service.run_task(push_payload)
    return result