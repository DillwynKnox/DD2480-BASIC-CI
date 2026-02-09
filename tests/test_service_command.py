from src.basic_ci.services.ServiceCommand import ServiceCommand
from pathlib import Path
import pytest
import subprocess

def test_run_echo_command():
    """
    This tests that "hello" is successfully returned
    """
    service = ServiceCommand()
    current_path = Path.cwd()
    result = service.run_command(["echo", "hello"], current_path)
    assert result.returncode == 0  # 0 means success
    assert "hello" in result.stdout
    
def test_command_error():
    """
    This tests that CalledProcessError is raised
    IN: Fake command
    OUT: CalledProcessError
    """
    service = ServiceCommand()
    with pytest.raises(subprocess.CalledProcessError):
        service.run_command(["ls", "/dwdwkdwodkodk"], Path("."))