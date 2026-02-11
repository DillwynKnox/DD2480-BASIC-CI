from git import Repo

from basic_ci.core.config import Settings, get_settings  #  git = gitPython package


class GitcloneService:
    """
    Clones a repo into a directory and checks out given commit.
    """
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
    
    def clone_repo(self, head_commit_hash: str, directory: str):
        
        repo = Repo.clone_from(self.repo_url, directory)
        repo.git.checkout(head_commit_hash)

    
def get_GitCloneService(settings:Settings = get_settings()) -> GitcloneService:
    """
    Factory for Gitclone Service    
    :param settings: Description
    :type settings: Settings
    :return: Description
    :rtype: GitcloneService
    """
    return GitcloneService(settings.REPO_URL)