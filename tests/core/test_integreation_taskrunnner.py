import shutil
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from basic_ci.core.config import Settings

# Replace 'your_module' with the actual filename
from basic_ci.core.TaskRunner import get_TaskRunner
from basic_ci.schemes.task import Task
from basic_ci.services.notification_service import NotificationService

DATA_DIR = Path(__file__).parent.parent / "data"



@pytest.fixture
def integration_task():
    """
    Using a real, small public repo to test the full clone and run cycle.
    """
    return Task(
        run_id="int-test-999",
        repo_url="https://github.com/DillwynKnox/DD2480-BASIC-CI", 
        branch="main",
        commit_sha="490c00335aa1e389ec118b7b2b9b148fbdb97a90"
    )

@pytest.fixture
def integreation_settings():
    """
    Settings for integration test, can be customized if needed.
    """
    return Settings(
        REPO_URL="https://github.com/DillwynKnox/DD2480-BASIC-CI",
        GITHUB_WEBHOOK_SECRET="dummytoken",
        GITHUB_TOKEN="dummytoken",
        PIPELINE_CONFIG_PATH=str(DATA_DIR / "integreation_pipeline.yaml"),
        SAVE_FOLDER = "pipeline_results/"
    )


def test_task_runner_full_integration(integration_task, integreation_settings):
    mock_notification = MagicMock(spec=NotificationService)

    runner = get_TaskRunner(settings=integreation_settings,notification_service=mock_notification)
    
    try:
        result = runner.run_task(integration_task)
        
        assert result.run_id == "int-test-999"
        assert result.status == "success"
      
        mock_notification.send_github_status.assert_called_once()    
    finally:
        temp_path = Path(f"/tmp/{integration_task.run_id}")
        if temp_path.exists():
            shutil.rmtree(temp_path)