from fastapi import FastAPI

from basic_ci.api.system import router as system_router
from basic_ci.api.webhook import router as webhook_router
from basic_ci.api.runs_API import router as runs_router
app = FastAPI()

@app.get("/")
def get_root() -> dict[str, str]:
    return {"message": "Basic CI pipeline is running"}

app.include_router(system_router)
app.include_router(webhook_router)
app.include_router(runs_router)