

import json
from dataclasses import asdict
from pathlib import Path

from basic_ci.core.config import Settings, get_settings
from basic_ci.schemes.TaskResult import TaskResult
from basic_ci.services.file_service import FileService, get_FileService


class Results_save_service:
    def __init__(self,file_service:FileService, settings:Settings = get_settings()):
        self.settings = settings
        self.file_service = file_service
        self.save_folder_path = Path(settings.SAVE_FOLDER)
    
    def save_task_result(self,task_result:TaskResult)-> None:
        """
        Saves the results of a Pipeline run

        Args:
            task_result (TaskResult): the result of the task
        Returns:
            None
        """
        task_save_path=self.save_folder_path / task_result.run_id
        
        self.file_service.create_folder(task_save_path)

        task_result_save_path = task_save_path / "taskResult.json"
        task_dict = asdict(task_result)
        
        with open(task_result_save_path,"w") as f:
            json.dump(task_dict,f,indent=2,default=str)



def get_Results_save_service(settings: Settings = get_settings())-> Results_save_service:
    """
    Factory for the Results saver service
    Args:
        settings (Settings, optional): The settings to use. Defaults to get_settings().
    Returns:
        Results_save_service: An instance of the Results_save_service
    """
    file_service = get_FileService()
    return Results_save_service(file_service=file_service,settings=settings)