from pathlib import Path
import pytest

from basic_ci.services.task_service import TaskService
from basic_ci.services.id_service import UIDService
from basic_ci.schemes.push_payload import Push_payload 


class MockUIDService(UIDService):
    """
    MockUIDService overrides run id generation to return a stable value for tests.
    """
    def generate_run_id(self, commit_hash=None, length=24) -> str:
        return f"run-{commit_hash}"


def _minimal_push_payload(ref: str = "refs/heads/main", after: str = "abc123") -> dict:
    """
    Returns the smallest payload that still validates against Push_payload.
    Adjust fields here only if Pydantic validation complains.
    """
    return {
        "ref": ref,
        "before": "000000",
        "after": after,
        "created": False,
        "deleted": False,
        "forced": False,
        "base_ref": None,
        "compare": "https://github.com/owner/repo/compare",
        "repository": {
            "id": 1,
            "node_id": "node",
            "name": "repo",
            "full_name": "owner/repo",
            "private": False,
            "owner": {"login": "owner", "id": 2},
            "html_url": "https://github.com/owner/repo",
            "description": None,
            "url": "https://api.github.com/repos/owner/repo",
        },
        "commits": [],
        "head_commit": None,
        "pusher": {"name": "alice", "email": None, "date": None},
        "sender": None,
    }
def _minimal_push_payload_obj(ref: str = "refs/heads/main", after: str = "abc123") -> Push_payload:
    """
    Returns the smallest valid Push_payload object for testing.
    """
    dict_payload = _minimal_push_payload(ref=ref, after=after)
    return Push_payload.model_validate(dict_payload)


def test_create_task():
    """
    test_create_task_happy_path verifies that TaskService creates a Task with the
    expected fields from a valid push payload.

    This is the primary success case test that validates the core functionality
    of the TaskService. It ensures that a valid GitHub push event payload
    results in a correctly populated Task object.
    
    :return: None
    """
    uid = MockUIDService()
    service = TaskService(uid)

    payload = _minimal_push_payload_obj(ref="refs/heads/main", after="deadbeef")
    task = service.create_task(payload)

    assert task.run_id == "run-deadbeef"
    assert task.branch == "main"
    assert task.commit_sha == "deadbeef"
    assert task.repo_url == "https://github.com/owner/repo"


def test_create_task_supports_nested_branch_names():
    """
    test_create_task_supports_nested_branch_names verifies that branch names containing
    slashes are extracted correctly (e.g., 'feature/x').

    This test ensures that the branch extraction logic properly handles nested
    branch names, which are common in Git workflows for features, releases,
    and hotfixes. It validates that the entire branch path is preserved,
    not just the last segment.
    
    :return: None
    """
    uid = MockUIDService()
    service = TaskService(uid)

    payload = _minimal_push_payload_obj(ref="refs/heads/feature/x", after="abc123")
    task = service.create_task(payload)

    assert task.branch == "feature/x"


def test_extract_branch_raises_on_non_head_ref():
    """
    test_extract_branch_raises_on_non_head_ref verifies that non-branch refs (tags, etc.)
    are rejected.

    This test validates error handling by ensuring that references which are
    not branches (such as Git tags) trigger an appropriate error. It confirms
    that the TaskService correctly distinguishes between branch references
    and other types of Git references.
    
    :return: None
    """
    uid = MockUIDService()
    service = TaskService(uid)

    payload = _minimal_push_payload_obj(ref="refs/tags/v1.0.0", after="abc123")

    with pytest.raises(ValueError):
        service.create_task(payload)
def test_task_is_immutable():
    """
    test_task_is_immutable verifies that Task objects are immutable (frozen dataclass).

    This test ensures that Task instances cannot be modified after creation,
    which is important for thread safety and predictable behavior in the CI
    pipeline. It validates that the @dataclass(frozen=True) decorator is
    functioning correctly.
    
    :return: None
    """
    uid = MockUIDService()
    service = TaskService(uid)
    
    payload = _minimal_push_payload_obj()
    task = service.create_task(payload)
    
    # Should fail because Task is frozen
    with pytest.raises(Exception):
        task.branch = "cannot-change-this"


def test_extract_branch_various_formats():
    """
    test_extract_branch_various_formats verifies that branch extraction works
    correctly with various Git reference formats.

    This comprehensive test validates the branch extraction logic against
    multiple common branch naming patterns, including simple branches,
    feature branches, hotfix branches, and release branches. It ensures
    robustness across different Git workflows.
    
    :return: None
    """
    uid = MockUIDService()
    service = TaskService(uid)
    
    test_cases = [
        ("refs/heads/main", "main"),
        ("refs/heads/develop", "develop"),
        ("refs/heads/feature/login-page", "feature/login-page"),
        ("refs/heads/fix/1.0.0", "fix/1.0.0"),
        ("refs/heads/feature/2.0.0", "feature/2.0.0"),
    ]
    
    for ref, expected in test_cases:
        payload = _minimal_push_payload_obj(ref=ref)
        task = service.create_task(payload)
        assert task.branch == expected, f"Failed for ref: {ref}"


def test_create_task_without_head_commit():
    """
    test_create_task_without_head_commit verifies that Task creation works
    correctly even when the payload does not contain a head_commit object.

    This test validates edge case handling by ensuring that the TaskService
    can process payloads where the 'head_commit' field is None. In such cases,
    the service should fall back to using the 'after' field as the commit SHA,
    which represents the new tip of the branch after the push.
    
    :return: None
    """
    uid = MockUIDService()
    service = TaskService(uid)
    
    payload = _minimal_push_payload_obj(after="sha_without_head_commit")
    # head_commit is already None in our helper
    task = service.create_task(payload)
    
    assert task.commit_sha == "sha_without_head_commit"
    assert task.branch == "main"


def test_unique_run_ids_for_different_commits():
    """
    test_unique_run_ids_for_different_commits verifies that different commit SHAs
    result in different run IDs being generated.

    This test ensures that the run ID generation is deterministic yet unique
    for different inputs. It validates that each CI run receives a distinct
    identifier, which is crucial for tracking, logging, and workspace isolation
    in the CI system.
    
    :return: None
    """
    uid = MockUIDService()
    service = TaskService(uid)
    
    # First task
    payload1 = _minimal_push_payload_obj(after="commit_abc")
    task1 = service.create_task(payload1)
    
    # Second task with different commit
    payload2 = _minimal_push_payload_obj(after="commit_def")
    task2 = service.create_task(payload2)
    
    assert task1.run_id == "run-commit_abc"
    assert task2.run_id == "run-commit_def"
    assert task1.run_id != task2.run_id