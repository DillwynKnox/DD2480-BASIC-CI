import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from basic_ci.core.config import Settings, get_settings
from basic_ci.schemes.task import Task
from basic_ci.schemes.TaskResult import TaskResult
from basic_ci.services.file_service import FileService, get_FileService
from basic_ci.services.gitclone_service import GitcloneService, get_GitCloneService
from basic_ci.services.notification_service import (
    NotificationService,
    get_NotificationService,
)
from basic_ci.services.pipeline_stage_service import (
    Pipeline_stage_service,
    get_Pipeline_stage_service,
)
from basic_ci.services.result_save_service import (
    Results_save_service,
    get_Results_save_service,
)
from basic_ci.services.ServiceCommand import ServiceCommand, get_ServiceCommand

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
    def __init__(self, file_service: FileService, 
                service_command: ServiceCommand, 
                notification_service: NotificationService, 
                git_service: GitcloneService , 
                pipeline_stage_service: Pipeline_stage_service,
                result_saver: Results_save_service,
                settings: Settings = get_settings()
                ):
        self.file_service = file_service
        self.service_command = service_command
        self.notification_service = notification_service
        self.git_service = git_service
        self.pipeline_stage_service = pipeline_stage_service
        self.result_saver = result_saver
        self.settings = settings

    def run_task(self,task: Task) ->TaskResult:
        """
        Runs a task given it's id.
        IN: Task (object)
        OUT: TaskResult (object)
        """
        started_at = datetime.now()

        temp_dir = Path(tempfile.gettempdir())
        task_folder = self.file_service.create_folder(temp_dir / task.run_id)
        
        self.git_service.clone_repo(task.commit_sha, task_folder)

        try:
            stage_results = self.pipeline_stage_service.run_stages(task_folder)
        except FileNotFoundError as e:
            stage_results=[]
            status = "failure"
            summary = f"pipeline.yaml not found: {e}"
        except ValueError as e:
            stage_results=[]
            status = "failure"
            summary = f"pipeline.yaml contains erros: {e}"

        for stage_result in stage_results:
            if not stage_result.success:
                status = "failure"
                summary = f" Stage {stage_result.name} failed"
                break
        else:
            if len(stage_results):
                status = "success"
                summary = "pipeline ran without errors"

        if temp_dir.exists():
            self.file_service.delete_folder(task_folder) 

        finished_at = datetime.now()
        task_result = TaskResult(
            run_id=task.run_id,
            repo_url=task.repo_url,
            branch = task.branch,
            commit_sha = task.commit_sha,
            status = status,
            started_at=started_at,
            finished_at=finished_at,
            stages = stage_results,
            summary=summary,
            details_url=self.settings.RESULTS_URL_TEMPLATE.format(run_id=task.run_id)
        )
        
        self.result_saver.save_task_result(task_result)
        self.notification_service.send_github_status(task_result)
        return task_result

def get_TaskRunner(settings:Settings = get_settings(),notification_service:Optional[NotificationService]=None) -> TaskRunner:
    """
    Factory for TaskRunner
    
    :param settings: A settinghs object defaults to the settings_factory
    :type settings: Settings

    :returns TaskRunner
    """
    fileService = get_FileService()
    command_service = get_ServiceCommand()
    git_service = get_GitCloneService(settings=settings)
    pipeline_stage_service = get_Pipeline_stage_service(settings= settings)
    if notification_service is None:
        notification_service = get_NotificationService(settings=settings)
    result_saver = get_Results_save_service(settings= settings)
    return TaskRunner(file_service=fileService,service_command=command_service, notification_service=notification_service, git_service=git_service, pipeline_stage_service=pipeline_stage_service, result_saver=result_saver,settings=settings)  

    