import json
from pathlib import Path

from basic_ci.core.config import Settings, get_settings
from basic_ci.schemes.TaskResult import TaskResult


class Read_results_service:
    def __init__(self, settings: Settings = get_settings()) -> None:
        self.settings = settings

    def get_task_result(self, run_id: str) -> TaskResult:
        """
        Reads the results of a given run from the file system
        Args:
            run_id (str): The ID of the run to read results for
        Returns:
            TaskResult: The results of the run as a TaskResult object
        """
        task_result_path = Path(self.settings.SAVE_FOLDER) / run_id / "taskResult.json"
  
        task_result_dict = json.load(task_result_path.open())
        return TaskResult(**task_result_dict)
    
    def get_all_runs(self) -> list[TaskResult]:
        """
        Reads the results of all runs from the file system
        Returns:
            list[TaskResult]: A list of TaskResult objects for all runs
        """
        runs: list[TaskResult] = []
        save_folder_path = Path(self.settings.SAVE_FOLDER)
        if not save_folder_path.exists():
            return runs
        
        for run_dir in save_folder_path.iterdir():
            if run_dir.is_dir():
                task_result_path = run_dir / "taskResult.json"
                if task_result_path.exists():
                    runs.append(self.get_task_result(run_dir.name))
        return runs
    

def get_Read_results_service(settings: Settings = get_settings()) -> Read_results_service:
    """
    Factory for the Read results service
    Args:
        settings (Settings, optional): The settings to use. Defaults to get_settings().
    Returns:
        Read_results_service: An instance of the Read_results_service
    """
    return Read_results_service(settings=settings)

