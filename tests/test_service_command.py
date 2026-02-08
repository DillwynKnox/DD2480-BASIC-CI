from src import get_os
from src.basic_ci.services.ServiceCommand import Service_command
from pathlib import Path

def test_run_echo_command():
    """
    This tests that "hello" is successfully returned
    """
    service = Service_command()
    current_path = Path.cwd()
    result = service.run_command(["echo", "hello"], current_path)
    assert result.returncode == 0  # 0 means success
    assert "hello" in result.stdout

def test_faulty_path():
    """
    This is a made up path that is supposed to be unsuccessful
    """
    service = Service_command()
    faulty_path = Path("/this/path/h&¤fff++")
    result = service.run_command(["ls", str(faulty_path)], Path.cwd())
    assert result.returncode != 0

    



