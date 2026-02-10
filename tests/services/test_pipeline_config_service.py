
from pathlib import Path

import pytest

from basic_ci.core.config import Settings
from basic_ci.services.pipeline_config_service import Pipeline_Config_service

DATA_DIR = Path(__file__).parent.parent / "data"
    

def test_non_existent_file():
    """
    Test that loading a non-existent pipeline configuration file raises FileNotFoundError.
    """
    settings = Settings(GITHUB_WEBHOOK_SECRET="dummy_secret", PIPELINE_CONFIG_PATH="non_existent_file.yaml")
    service = Pipeline_Config_service(settings=settings)
    with pytest.raises(FileNotFoundError):
        service.load_pipeline_config()

def test_valid_pipeline_config():
    """
    Test that a valid pipeline configuration file is loaded correctly.
    """
    correct_pipeline_path = DATA_DIR / "correct_pipeline.yaml"
    settings = Settings(GITHUB_WEBHOOK_SECRET="dummy_secret", PIPELINE_CONFIG_PATH=str(correct_pipeline_path))
    service = Pipeline_Config_service(settings=settings)
    pipeline_config = service.load_pipeline_config()
    
    assert pipeline_config.project == "unittest"
    assert len(pipeline_config.stages) == 1
    assert pipeline_config.stages[0].stage == "setup"
    assert pipeline_config.stages[0].command == 'echo "Setting up the environment..."'

def test_malformed_pipeline_config():
    """
    Test that loading a malformed pipeline configuration file raises ValueError.
    """
    malformed_pipeline_path = DATA_DIR / "wrong_pipeline.yaml"
    settings = Settings(GITHUB_WEBHOOK_SECRET="dummy_secret", PIPELINE_CONFIG_PATH=str(malformed_pipeline_path))
    service = Pipeline_Config_service(settings=settings)
    with pytest.raises(ValueError):
        service.load_pipeline_config()