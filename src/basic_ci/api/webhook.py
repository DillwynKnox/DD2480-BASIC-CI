from fastapi import APIRouter, Header
from fastapi.params import Depends

from basic_ci.core.signature import Signature_verifier, get_signature_verifier
from basic_ci.schemes.push_payload import Push_payload
from basic_ci.schemes.TaskResult import TaskResult
from basic_ci.services.task_service import TaskService, get_TaskService

router = APIRouter(tags=["webhook"])

@router.post("/webhook")
async def handle_webhook(
    push_payload: Push_payload,  
    x_hub_signature_256: str = Header(...), 
    verifier: Signature_verifier = Depends(get_signature_verifier),
    task_service: TaskService = Depends(get_TaskService)
) -> TaskResult:
    """Verifyies Signature and extract payload from incoming github webhook payloads."""
    print(f"Received webhook for repo: {push_payload.repository.full_name}")
    return task_service.run_task(push_payload)