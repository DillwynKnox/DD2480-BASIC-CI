
import requests

from basic_ci.services.TaskResult import TaskResult


class NotificationService:
    """
    Sends CI results back to GitHub (commit statuses).
    Later it can be extended to email / Slack, etc.
    """

    def __init__(self, github_token: str, github_api_base: str = "https://api.github.com"):
        """
        Initialize the NotificationService with GitHub API credentials.

        Args:
            github_token (str): GitHub personal access token for API authentication.
                               Requires repo:status scope for public repositories,
                               or repo scope for private repositories.
            github_api_base (str): Base URL for GitHub API. Defaults to
                                  "https://api.github.com". Can be overridden for
                                  GitHub Enterprise instances.

        Returns:
            None
        """

        self.github_token = github_token
        self.github_api_base = github_api_base.rstrip("/")

    def send_github_status(
        self,
        task_result: TaskResult,
        context: str = "basic-ci",
    ) -> None:
        """
        Create or update a GitHub commit status for the commit SHA.

        This method posts a commit status to GitHub using the Checks API.
        The status appears in pull requests, commit history, and can be used
        to enforce required status checks before merging.

        Args:
            task_result (TaskResult): Result object containing the CI run results,
                                     including commit SHA, repository URL, and status.
            context (str): Label that identifies the status check in GitHub UI.
                          Defaults to "basic-ci". Useful when multiple CI systems
                          report statuses for the same commit.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If the GitHub API request fails
            ValueError: If the repository URL cannot be parsed or is not from GitHub
            KeyError: If the task_result is missing required fields

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
        """
        Map internal CI status to GitHub commit status state.

        GitHub accepts four states: 'success', 'failure', 'error', and 'pending'.
        Any unknown or empty status is mapped to 'error' for safety.

        Args:
            status (str): Internal CI status (e.g., "success", "failed", "pending")

        Returns:
            str: GitHub-compatible state string ('success', 'failure', 'error', or 'pending')
        """
        s = (status or "").lower()
        if s in {"success", "failure", "error", "pending"}:
            return s
        return "error"

    @staticmethod
    def _parse_github_repo(repo_url: str) -> tuple[str, str]:
        """
        Extract owner and repository name from a GitHub URL.

        Supports multiple GitHub URL formats:
        - HTTPS: https://github.com/owner/repo or https://github.com/owner/repo.git
        - SSH: git@github.com:owner/repo or git@github.com:owner/repo.git
        - API: https://api.github.com/repos/owner/repo

        Args:
            repo_url (str): GitHub repository URL in any supported format

        Returns:
            Tuple[str, str]: A tuple containing (owner, repository_name)

        Raises:
            ValueError: If the URL format is not supported or cannot be parsed
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
