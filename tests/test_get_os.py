import pytest
from src import get_os

def test_win_os_is_win():
    """
    This was tested on a windows computer.
    """
    assert get_os.get_os_type() == "Windows"

def test_fake_prefix():
    """
    This tests that a operating system prefix that isn't Windows, Mac, or Linux
    is incompatible. 
    """
    assert get_os.get_os_type("xyz") == "Incompatible" 

def test_win_os_command():
    """
    This was tested on a windows computer.
    """
    assert get_os.get_terminal_os_command("Windows") == ["wsl"] 

def test_invalid_os_raises():
    with pytest.raises(ValueError):
        get_os.get_terminal_os_command(-1)