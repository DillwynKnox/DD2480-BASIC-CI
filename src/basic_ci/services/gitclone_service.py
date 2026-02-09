from git import Repo #  git = gitPython package


class GitcloneService:
    """
    Clones a repo into a directory and checks out given commit.
    """
    def __init__(self, repo_url: str, head_commit_hash: str, directory: str):
        self.repo_url = repo_url
        self.commit_hash = head_commit_hash
        self.directory = directory
    
    def clone_repo(self):
        repo = Repo.clone_from(self.repo_url, self.directory)
        repo.git.checkout(self.commit_hash)

    
    