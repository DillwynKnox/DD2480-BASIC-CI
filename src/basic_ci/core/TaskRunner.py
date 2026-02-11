import tempfile
from pathlib import Path

from basic_ci.schemes.task import Task
from basic_ci.schemes.TaskResult import TaskResult
from basic_ci.services.file_service import FileService
from basic_ci.services.pipeline_stage_service import Pipeline_stage_service

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
    def __init__(self, file_service: FileService, service_command, notification_service, git_service, pipeline_stage_service: Pipeline_stage_service):
        self.file_service = file_service
        self.service_command = service_command
        self.notification_service = notification_service
        self.git_service = git_service
        self.pipeline_stage_service = pipeline_stage_service

    def run_task(self, task: Task):
        """
        Runs a task given it's id.
        IN: task_id (str)
        OUT: TaskResult (object)
        """
        
        task_result = TaskResult()

        temp_dir = Path(tempfile.gettempdir())
        task_folder = self.file_service.create_folder(temp_dir / task.task_id)

        after_commit_hash = self.task.get_head_hash(task.after_commit)
        
        self.git_service.clone(task_folder,
                               after_commit_hash = self.task.get_head_hash(Task.after_commit))

        self.pipeline_stage_service 

        if temp_dir.exists():
            self.file_service.delete_folder(temp_dir) 
        
        self.notification_service.send_github_status(task_result)
        return task_result

