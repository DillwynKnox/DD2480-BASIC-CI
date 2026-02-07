import sys

def get_os_type():
    """
    Get the type of operating system on this computer
    Thee os HAS to be Windows (use wsl terminal) or Linux or Mac
    OUT: os system type
    """
    if sys.platform.startswith("win"):
        return "Windows"
    elif sys.platform.startswith("linux"):
        return "Linux"
    elif sys.platform.startswith("darwin"):
        return "Mac"

def get_terminal_os_command(operating_system):
    """
    Get the type of terminal based on operating system
    IN: operating system type (str)
    OUT: terminal command type (str)
    """

    if operating_system == "Windows":
        return ["wsl"]
    elif operating_system == "Linux":
        return ["/bin/bash"]
    elif operating_system == "Mac":
        return ["/bin/zsh"]