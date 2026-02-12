from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    """
    Task represents a single CI run created from a GitHub webhook payload.
    It contains all information required by the TaskRunner to execute the CI pipeline.
    """
    run_id: str
    repo_url: str
    branch: str
    commit_sha: str