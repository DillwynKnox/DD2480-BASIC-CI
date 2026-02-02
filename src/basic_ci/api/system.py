from importlib.metadata import PackageNotFoundError, version

from fastapi import APIRouter

router = APIRouter(tags=["system"])

@router.get("/version")
def get_version() -> dict[str, str]:
    """Get the current version of the Basic CI package."""
    try:
        pkg_version = version("basic-ci")
    except PackageNotFoundError:
        pkg_version = "unknown"
    return {"version": pkg_version}

@router.get("/health")
def get_health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}