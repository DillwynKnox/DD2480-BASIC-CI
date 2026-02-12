from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from basic_ci.services.read_results_service import (
    Read_results_service,
    get_Read_results_service,
)

router = APIRouter(tags=["runs"])
templates = Jinja2Templates(directory="src/basic_ci/templates")



@router.get("/runs/{run_id}")
def run_details_page(request: Request, run_id: str, db: Read_results_service = Depends(get_Read_results_service)) -> _TemplateResponse:
    task_result = db.get_task_result(run_id)
    if not task_result:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")

    # Render HTML page
    return templates.TemplateResponse(
        "run_details.html",
        {
            "request": request,     # REQUIRED by Jinja2Templates
            "run": task_result,     # pass TaskResult to template
        },
    )
