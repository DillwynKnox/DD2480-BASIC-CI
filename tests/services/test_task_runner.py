<<<<<<< HEAD
from unittest.mock import MagicMock
=======
from pathlib import Path
from unittest.mock import MagicMock, _patch
>>>>>>> 29-feat-task_runner-that-runs-the-actual

import pytest

from basic_ci.core.TaskRunner import TaskRunner
<<<<<<< HEAD
=======
from basic_ci.schemes.task import Task
from basic_ci.schemes.TaskResult import TaskResult
>>>>>>> 29-feat-task_runner-that-runs-the-actual


@pytest.fixture
def mock_services():
    return {
        "file_service": MagicMock(),
        "command_service": MagicMock(),
        "notification_service": MagicMock(),
        "git_service": MagicMock(),
        "pipeline_service": MagicMock(),
    }

@pytest.fixture
def task_runner(mock_services):
    return TaskRunner(
        file_service=mock_services["file_service"],
        service_command=mock_services["command_service"],
        notification_service=mock_services["notification_service"],
        git_service=mock_services["git_service"],
        pipeline_stage_service=mock_services["pipeline_service"]
    )
