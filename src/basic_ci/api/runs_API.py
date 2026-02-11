from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

from basic_ci.services.dummy_database_service import DummyDatabaseService
from basic_ci.services.TaskResult import TaskResult

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dummy DB instance (mockable / replaceable later)
db = DummyDatabaseService()




@router.get("/runs/{run_id}")
def run_details_page(request: Request, run_id: str):
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
