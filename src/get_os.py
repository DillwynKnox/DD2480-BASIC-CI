import sys

def get_os_type(_platform=sys.platform): #Do Not remove parameter, it's for testing
    """
    Get the type of operating system on this computer
    Thee os HAS to be Windows (use wsl terminal) or Linux or Mac
    OUT: os system type
    """
    if _platform.startswith("win"):
        return "Windows"
    elif _platform.startswith("linux"):
        return "Linux"
    elif _platform.startswith("darwin"):
        return "Mac"
    else:
        return "Incompatible"

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
    else:
        raise ValueError