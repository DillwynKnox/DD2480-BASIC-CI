from basic_ci.services.gitclone_service import GitcloneService
import pytest
from unittest.mock import MagicMock, patch


def test_clone_repo_calls_git_correctly():
    """
    Tests that all methods from GitcloneService are called correctly when an object is created and clone_repo() is run.
    """
    with patch("basic_ci.services.gitclone_service.Repo") as mock_repo_class:
        mock_repo_instance = MagicMock()
        mock_repo_class.clone_from.return_value = mock_repo_instance

        service = GitcloneService(
            repo_url="https://github.com/example/fakerepo.git")

        service.clone_repo(head_commit_hash="123456",
            directory="/fake/repo")

        mock_repo_class.clone_from.assert_called_once_with(
            "https://github.com/example/fakerepo.git",
            "/fake/repo",
        )
        mock_repo_instance.git.checkout.assert_called_once_with("123456")



