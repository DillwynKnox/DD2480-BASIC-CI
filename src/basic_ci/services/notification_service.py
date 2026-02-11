
import requests

from basic_ci.core.config import Settings, get_settings
from basic_ci.schemes.TaskResult import TaskResult


class NotificationService:
    """
    Sends CI results back to GitHub (commit statuses).
    Later it can be extended to email / Slack, etc.
    """

    def __init__(self, github_token: str, github_api_base: str = "https://api.github.com"):
        self.github_token = github_token
        self.github_api_base = github_api_base.rstrip("/")

    def send_github_status(
        self,
        task_result: TaskResult,
        context: str = "basic-ci",
    ) -> None:
        """
        Creates a GitHub commit status on the commit SHA.
        """

        state = self._map_state(task_result.status) 

        description = task_result.summary or f"CI finished with status: {task_result.status}"
        if len(description) > 140:
            description = description[:137] + "..."

        payload = {
            "state": state,
            "context": context,
            "description": description,
        }

        if task_result.details_url:
            payload["target_url"] = task_result.details_url

        owner, repo = self._parse_github_repo(task_result.repo_url)
        url = f"{self.github_api_base}/repos/{owner}/{repo}/statuses/{task_result.commit_sha}"

        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()

    @staticmethod
    def _map_state(status: str) -> str:
        s = (status or "").lower()
        if s in {"success", "failure", "error", "pending"}:
            return s
        return "error"

    @staticmethod
    def _parse_github_repo(repo_url: str) -> tuple[str, str]:
        """
        Supports:
        - https://github.com/OWNER/REPO(.git)
        - git@github.com:OWNER/REPO(.git)
        """
        repo_url = repo_url.strip()

        if repo_url.startswith("git@github.com:"):
            path = repo_url.split("git@github.com:", 1)[1]
        elif "github.com/" in repo_url:
            path = repo_url.split("github.com/", 1)[1]
        else:
            raise ValueError(f"Unsupported repo url: {repo_url}")

        path = path.rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]

        owner, repo = path.split("/", 1)
        return owner, repo

def get_NotificationService(settings: Settings = get_settings())-> NotificationService:
    """
    Factory for Notification Service    
    :param settings: the general Config
    :type settings: Settings
    :return: a new instance of Settings 
    :rtype: NotificationService
    """
    return NotificationService(settings.GITHUB_TOKEN)