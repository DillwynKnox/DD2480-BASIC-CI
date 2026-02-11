import tempfile
from pathlib import Path

from basic_ci.schemes.task import Task
from basic_ci.schemes.TaskResult import TaskResult
from basic_ci.services.file_service import FileService
from basic_ci.services.gitclone_service import GitcloneService
from basic_ci.services.notification_service import NotificationService
from basic_ci.services.pipeline_stage_service import Pipeline_stage_service
from basic_ci.services.ServiceCommand import ServiceCommand



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
    def __init__(self, file_service: FileService, service_command: ServiceCommand, notification_service: NotificationService, git_service: GitcloneService , pipeline_stage_service: Pipeline_stage_service):
        self.file_service = file_service
        self.service_command = service_command
        self.notification_service = notification_service
        self.git_service = git_service
        self.pipeline_stage_service = pipeline_stage_service

    def run_task(self, task: Task) ->TaskResult:
        """
        Runs a task given it's id.
        IN: Task (object)
        OUT: TaskResult (object)
        """

        temp_dir = Path(tempfile.gettempdir())
        task_folder = self.file_service.create_folder(temp_dir / task.commit_sha)
        
        self.git_service.clone_repo(task.commit_sha, task_folder)

        self.pipeline_stage_service() 

        if temp_dir.exists():
            self.file_service.delete_folder(temp_dir) 

        task_result = TaskResult(task.run_id, task.repo_url, task.branch, task.commit_sha, task.status)
        self.notification_service.send_github_status(task_result)
        return task_result

