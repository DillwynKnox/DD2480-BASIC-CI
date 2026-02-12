import json
from pathlib import Path

from basic_ci.core.config import Settings, get_settings
from basic_ci.schemes.TaskResult import TaskResult
from basic_ci.services.file_service import FileService


class Read_results_service:
    def __init__(self, file_service: FileService, settings: Settings = get_settings()):
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
        if not task_result_path.exists():
            return None 
        task_result_dict = json.load(task_result_path.open())
        return TaskResult(**task_result_dict)
    

def get_Read_results_service(settings: Settings = get_settings()) -> Read_results_service:
    """
    Factory for the Read results service
    Args:
        settings (Settings, optional): The settings to use. Defaults to get_settings().
    Returns:
        Read_results_service: An instance of the Read_results_service
    """
    file_service = FileService()
    return Read_results_service(file_service=file_service, settings=settings)