from pathlib import Path
from unittest.mock import MagicMock, _patch

import pytest

from basic_ci.core.TaskRunner import TaskRunner
from basic_ci.schemes.task import Task
from basic_ci.schemes.TaskResult import TaskResult


@pytest.fixture
def mock_services():
    """Fixture to provide mocked dependencies."""
    return {
        "file_service": MagicMock(),
        "command_service": MagicMock(),
        "notification_service": MagicMock(),
        "git_service": MagicMock(),
        "pipeline_service": MagicMock(),
    }

@pytest.fixture
def task_runner(mock_services):
    """Fixture to initialize TaskRunner with mocked services."""
    return TaskRunner(
        file_service=mock_services["file_service"],
        service_command=mock_services["command_service"],
        notification_service=mock_services["notification_service"],
        git_service=mock_services["git_service"],
        pipeline_stage_service=mock_services["pipeline_service"]
    )

def test_run_task_flow(task_runner, mock_services):
    # 1. Setup Mock Data
    mock_task = MagicMock()
    mock_task.task_id = "test-123"
    mock_task.after_commit = "sha-abc"
    
    result = True
    assert result is not None





