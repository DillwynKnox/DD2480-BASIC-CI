import tempfile
from dataclasses import dataclass
from pathlib import Path

from basic_ci.schemes.task import Task
from basic_ci.services.file_service import FileService
from basic_ci.services.id_service import UIDService
from basic_ci.services.notification_service import NotificationService
from basic_ci.services.TaskResult import CommandResult, TaskResult

"""
- Get Task Object from Task Service
Create new Folder named after unique id in temp location with FileService
Clone Git Repo with GitService
? Run commands (setup -> static typecheck -> pytest -> build) uses Command Service (Will be done in different serivce).
Create TaskResult object.
Send TaskResult Object to Notification Service
"""

class TaskRunner:
    """
    Run the actual task itself, by coordinating the other basic_ci services.
    """
    def __init__(self, task, id_service, file_service, service_command, notification_service, git_service):
        self.task = task
        self.id_service = id_service
        self.file_service = file_service
        self.service_command = service_command
        self.notification_service = notification_service
        self.git_service = git_service

    def run_task(self, task_id):
        """
        Runs a task given it's id.
        IN: task_id (str)
        OUT: TaskResult (object)
        """
        temp_dir = Path(tempfile.gettempdir())
        
        file_service = file_service.FileService(base_workspace=temp_dir)
        task_folder = file_service.create_folder(temp_dir / task_id)

        self.git_service.clone(task_folder)

        #Pipeline will run commands

        task_result = TaskResult.TaskResult()

        if temp_dir.exists():
            file_service.delete_folder(temp_dir) 
            
        return self.notification_service.send_github_status(task_result)

