from typing import Optional, Dict
from basic_ci.services.TaskResult import TaskResult

class DummyDatabaseService:
    """
    Mockable dummy DB for now. Later replace with real persistence.
    """
    def __init__(self) -> None:
        self._store: Dict[str, TaskResult] = {}

    def save(self, task_result: TaskResult) -> None:
        self._store[task_result.run_id] = task_result

    def get_task_result(self, run_id: str) -> Optional[TaskResult]:
        return self._store.get(run_id)
