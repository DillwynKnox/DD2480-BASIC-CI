from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from basic_ci.schemes.stage_result import Stage_result


@dataclass
class TaskResult:
    """
    Stores relevant information related to a specific run of the CI server.
    Used by NotificationService.send_github_status() to send information to github.
    """
    
    run_id: str
    repo_url: str
    branch: str
    commit_sha: str

    status: str
    started_at:  Optional[datetime] = None
    finished_at: Optional[datetime] = None

    stages: List[Stage_result] = field(default_factory=list)
    summary: str = ""
    details_url: Optional[str] = None  # later: /builds/<run_id> or similar

    def is_success(self) -> bool:
        return self.status == "success"
