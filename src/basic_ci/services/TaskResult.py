from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class CommandResult:
    name: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""


@dataclass
class TaskResult:
    run_id: str
    repo_url: str
    branch: str
    commit_sha: str

    status: str  # "success" | "failure" | "pending" | "error"
    started_at: datetime = field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None

    commands: List[CommandResult] = field(default_factory=list)
    summary: str = ""
    details_url: Optional[str] = None  # later: /builds/<run_id> or similar

    def is_success(self) -> bool:
        return self.status == "success"
