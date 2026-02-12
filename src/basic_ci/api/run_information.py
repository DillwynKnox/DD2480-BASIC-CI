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
    """
    Endpoint to render the details page for a specific run.
    Args:
        request (Request): The incoming HTTP request, required for template rendering.
        run_id (str): The ID of the run to display details for.
        db (Read_results_service, optional): Dependency-injected service to read results. Defaults to get_Read_results_service().
    Returns:
        _TemplateResponse: The rendered HTML page with run details.
    """
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


@router.get("/runs")
def runs_overview_page(
    request: Request, 
    db: Read_results_service = Depends(get_Read_results_service)
) -> _TemplateResponse:
    """
    Endpoint to render an overview page of all pipeline runs.
    
    Args:
        request (Request): The incoming HTTP request, required for template rendering.
        db (Read_results_service): Dependency-injected service to read results.
    
    Returns:
        _TemplateResponse: The rendered HTML page with all runs.
    """
    all_runs = db.get_all_runs()
    sorted_runs = sorted(
        all_runs, 
        key=lambda x: x.started_at if x.started_at else "", 
        reverse=True
    )
    
    return templates.TemplateResponse(
        "all_runs.html",
        {
            "request": request,
            "runs": sorted_runs,
        },
    )
