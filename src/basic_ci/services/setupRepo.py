import subprocess
from pathlib import Path
from git import Repo #  It is the gitPython package
import sys



def clone_and_setup_repo(repo_url: str, branch: str, base_directory: str):
    """
    Creates a new local folder, clones git repo to it and sets it up on server
    
    :param repo_url: The url for the repo
    :type repo_url: str
    :param branch: Branch name
    :type branch: str
    :param base_directory: The base directory of the CI server where builds should be installed
    :type base_directory: str
    """
    # Make new directory
    build_path = Path(base_directory) / branch
    build_path.mkdir(parents=True, exist_ok=True)
    
    # Clone branch
    Repo.clone_from(repo_url, build_path, branch=branch)
    
    # Build project
    pyproject = build_path / "pyproject.toml"
    if pyproject.exists():
        
        # Install uv
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        
        # Install dependencies using uv
        print("Installing dependencies via uv...")
        subprocess.run(["uv", "sync", "--extra", "dev"], cwd=build_path, check=True)
        
    return build_path
    
    