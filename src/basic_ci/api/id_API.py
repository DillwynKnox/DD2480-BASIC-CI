from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from src.basic_ci.services.id_service import make_run_id

app = FastAPI()

class RunRequest(BaseModel):
    commit_hash: str | None = None

@app.post("/run-id")
def create_run_id(body: RunRequest):
    run_id = make_run_id(body.commit_hash)
    return {"run_id": run_id}
