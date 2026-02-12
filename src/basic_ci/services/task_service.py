from __future__ import annotations

from fastapi import Depends

from basic_ci.core.config import Settings, get_settings
from basic_ci.core.TaskRunner import TaskRunner, get_TaskRunner
from basic_ci.schemes.push_payload import Push_payload
from basic_ci.schemes.task import Task
from basic_ci.schemes.TaskResult import TaskResult
from basic_ci.services.id_service import UIDService


class TaskService:
    """
    TaskService is responsible for creating Task objects from GitHub webhook payloads.
    It does not execute tasks; it only prepares them.
    """

    def __init__(self, uid_service: UIDService, task_runner: TaskRunner):
        """
        Initialize the TaskService with a UID service.

        Args:
            uid_service (UIDService): Service responsible for generating unique run IDs
            
        Returns:
            None
        """
        self.uid_service = uid_service
        self.task_runner = task_runner
    def create_task(self, payload: Push_payload) -> Task:
        """
        Convert a validated Push_payload object into a Task object.

        This method extracts the branch name, commit SHA, and repository URL from
        the payload, generates a unique run ID, and creates a Task object with
        all information needed for CI execution.

        Args:
            payload (Push_payload): Validated Push_payload object from GitHub webhook

        Returns:
            Task: Task object containing run_id, repo_url, branch, and commit_sha

        Raises:
            ValueError: If the payload is missing required fields or contains
                       invalid data (e.g., non-branch ref format)
        """
        

        branch = self._extract_branch(payload.ref)
        commit_sha = payload.after
        repo_url = self._extract_repo_url(payload)
        run_id = self.uid_service.generate_run_id(commit_hash=commit_sha)

        return Task(
            run_id=run_id,
            repo_url=repo_url,
            branch=branch,
            commit_sha=commit_sha,
        )
    
    def run_task(self, push_payload: Push_payload) -> TaskResult:
        """
        Runs the actual task.
        :param self: Description
        :param task: Description
        :type task: Task
        :return: Description
        :rtype: Any
        """
        task = self.create_task(push_payload)
        return self.task_runner.run_task(task)


    def _extract_branch(self, ref: str) -> str:
        """
        Extract the branch name from a Git reference string.

        Args:
            ref (str): Git reference string (e.g., 'refs/heads/main', 
                      'refs/heads/feature/login-page')

        Returns:
            str: Branch name (e.g., 'main', 'feature/login-page')

        Raises:
            ValueError: If the ref format is unexpected (doesn't start with 
                       'refs/heads/') or is empty
        """
        PREFIX = "refs/heads/"
        
        if not ref.startswith(PREFIX):
            raise ValueError(f"Unexpected ref format: {ref}")
        return ref.replace(PREFIX, "", 1)

    def _extract_repo_url(self, pp: Push_payload) -> str:
        """
        Extract a repository URL suitable for cloning from the payload.

        Currently uses the html_url field from the repository object.
        GitHub automatically handles the .git suffix when cloning from html_url.
        This can be updated to use clone_url/ssh_url if those fields are added
        to the Repository model later.

        Args:
            pp (Push_payload): Parsed Push_payload object

        Returns:
            str: Repository URL string for cloning
        """
        # Currently your Repository model exposes html_url.
        # This is acceptable for now; clone_url/ssh_url can be added later.
        return pp.repository.html_url

def get_TaskService(settings: Settings = Depends(get_settings)) -> TaskService:
    """
    Factory for Task Service    
    :param settings: the general Config
    :type settings: Settings
    :return: a new instance of Settings 
    :rtype: TaskService
    """
    uid_service = UIDService()
    task_runner = get_TaskRunner(settings=settings)
    return TaskService(uid_service=uid_service, task_runner=task_runner)