from unittest.mock import MagicMock

from basic_ci.schemes.pipeline import PipelineConfig, Stage
from basic_ci.services.pipeline_stage_service import Pipeline_stage_service


def test_pipeline_execution_logic(tmp_path):
    """
    Checks if the service correctly retrieves stages from the config, 
    executes the commands via the command_service, and maps the results.
    """
    mock_command_service = MagicMock()
    mock_config_service = MagicMock()
    
    service = Pipeline_stage_service(mock_command_service, mock_config_service)
    
    real_stages = [
        Stage(stage="Lint", command="ruff ."),
        Stage(stage="Test", command="pytest")
    ]
    mock_config_service.load_pipeline_config.return_value = PipelineConfig(
        project="test-project", 
        stages=real_stages
    )
    
    res_success = MagicMock(returncode=0, stdout="OK", stderr="")
    res_fail = MagicMock(returncode=1, stdout="", stderr="Error")
    mock_command_service.run_command.side_effect = [res_success, res_fail]

    results = service.run_stages(str(tmp_path))

    assert len(results) == 2
    assert results[0].name == "Lint"
    assert results[0].success is True
    assert results[1].name == "Test"
    assert results[1].success is False
    
    assert mock_command_service.run_command.call_count == 2
    mock_command_service.run_command.assert_any_call(["ruff", "."], path=tmp_path)