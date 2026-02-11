from git import Repo #  git = gitPython package


class GitcloneService:
    """
    Clones a repo into a directory and checks out given commit.
    """
    def __init__(self, repo_url: str) -> None:
        self.repo_url = repo_url
    
    def clone_repo(self, head_commit_hash: str, directory: str) -> None:
        
        repo = Repo.clone_from(self.repo_url, directory)
        repo.git.checkout(head_commit_hash)

    
    