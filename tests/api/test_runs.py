from unittest.mock import Mock, patch

from basic_ci.api.run_information import run_details_page


def test_run_details_page_success():
    """Test successful retrieval and rendering of run details."""
    mock_request = Mock()
    run_id = "test-run-123"
    mock_task_result = Mock()
    mock_db = Mock()
    mock_db.get_task_result.return_value = mock_task_result
    
    with patch('basic_ci.api.run_information.templates') as mock_templates:
        run_details_page(mock_request, run_id, mock_db)
        
        # Assert
        mock_db.get_task_result.assert_called_once_with(run_id)
        mock_templates.TemplateResponse.assert_called_once_with(
            "run_details.html",
            {"request": mock_request, "run": mock_task_result}
        )