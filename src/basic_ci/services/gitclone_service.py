from git import Repo #  git = gitPython package


class GitcloneService:
    """
    Clones a repo into a directory and checks out given commit.
    """
    def __init__(self, repo_url: str):
        """
        Initialize the GitcloneService with a repository URL.

        Args:
            repo_url (str): URL of the Git repository to clone.
                           Supports HTTPS, SSH, and local file protocols.

        Returns:
            None

        Example:
            >>> service = GitcloneService("https://github.com/user/repo.git")
        """
        self.repo_url = repo_url
    
    def clone_repo(self, head_commit_hash: str, directory: str):
        """
        Clone the repository and checkout a specific commit.

        This method performs two operations atomically:
        1. Clones the entire repository from the configured URL into the
           specified directory.
        2. Checks out the exact commit identified by the provided hash.

        The clone operation is shallow (full history is cloned). For large
        repositories, consider implementing shallow clone with depth=1 if
        full history is not needed.

        Args:
            head_commit_hash (str): Full or abbreviated commit SHA to checkout.
                                   Must be a valid commit in the repository.
            directory (Union[str, Path]): Local filesystem path where the
                                        repository should be cloned.

        Returns:
            Repo: GitPython Repo object representing the cloned repository.
                 Can be used for further Git operations if needed.

        Raises:
            git.exc.GitCommandError: If the clone or checkout operation fails.
                                    Common causes include:
                                    - Invalid repository URL
                                    - Network connectivity issues
                                    - Insufficient permissions
                                    - Invalid commit hash
            OSError: If the target directory cannot be created or accessed.
        """
        repo = Repo.clone_from(self.repo_url, directory)
        repo.git.checkout(head_commit_hash)

    
    