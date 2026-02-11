from __future__ import annotations

from basic_ci.schemes.push_payload import Push_payload
from basic_ci.schemes.task import Task
from basic_ci.services.id_service import UIDService


class TaskService:
    """
    TaskService is responsible for creating Task objects from GitHub webhook payloads.
    It does not execute tasks; it only prepares them.
    """

    def __init__(self, uid_service: UIDService):
        """
        __init__ initializes the TaskService.

        :param uid_service: Service responsible for generating unique run IDs
        :return: None
        """
        self.uid_service = uid_service

    def create_task(self, payload: Push_payload) -> Task:
        """
        create_task validates a webhook payload and converts it into a Task object.

        :param payload: Validated Push_payload object from GitHub webhook
        :return: Task object containing run_id, repo_url, branch, commit_sha
        :raises ValueError: If the payload is invalid or missing required fields
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


    def _extract_branch(self, ref: str) -> str:
        """
        Extracts the branch name from a Git reference string.

        :param ref: Git ref string (e.g. 'refs/heads/main')
        :return: Branch name (e.g. 'main')
        :raises ValueError: If the ref format is unexpected
        """
        PREFIX = "refs/heads/"
        
        if not ref.startswith(PREFIX):
            raise ValueError(f"Unexpected ref format: {ref}")
        return ref.replace(PREFIX, "", 1)

    def _extract_repo_url(self, pp: Push_payload) -> str:
        """
        Extracts a repository URL suitable for cloning.

        :param pp: Parsed Push_payload object
        :return: Repository URL string
        """
        # Currently your Repository model exposes html_url.
        # This is acceptable for now; clone_url/ssh_url can be added later.
        return pp.repository.html_url
