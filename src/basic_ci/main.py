from fastapi import FastAPI

from basic_ci.api.system import router as system_router

app = FastAPI()

@app.get("/")
def get_root() -> dict[str, str]:
    return {"message": "Basic CI pipeline is running"}

app.include_router(system_router)