
from dataclasses import dataclass


@dataclass
class Task:
    task_id: str
    head_commit: str
    after_commit: str
