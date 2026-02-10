from datetime import datetime
from unittest.mock import MagicMock, patch

from basic_ci.services.notification_service import NotificationService
from basic_ci.services.TaskResult import TaskResult


def test_send_github_status_builds_correct_request():
    service = NotificationService(github_token="FAKE_TOKEN")

    task_result = TaskResult(
        run_id="abc123",
        repo_url="https://github.com/OWNER/REPO",
        branch="assessment",
        commit_sha="0123456789abcdef0123456789abcdef01234567",
        status="success",
        started_at=datetime.now(),
        finished_at=datetime.now(),
        summary="All steps succeeded",
        details_url="https://example.com/builds/abc123",
        commands=[],
    )

    with patch("basic_ci.services.notification_service.requests.post") as post_mock:
        fake_resp = MagicMock()
        fake_resp.raise_for_status.return_value = None
        post_mock.return_value = fake_resp

        service.send_github_status(task_result, context="basic-ci")

        assert post_mock.call_count == 1

        args, kwargs = post_mock.call_args
        url = args[0]
        json_payload = kwargs["json"]
        headers = kwargs["headers"]

        assert url == "https://api.github.com/repos/OWNER/REPO/statuses/0123456789abcdef0123456789abcdef01234567"

        assert headers["Authorization"] == "Bearer FAKE_TOKEN"
        assert "application/vnd.github+json" in headers["Accept"]

        assert json_payload["state"] == "success"
        assert json_payload["context"] == "basic-ci"
        assert json_payload["description"] == "All steps succeeded"
        assert json_payload["target_url"] == "https://example.com/builds/abc123"
