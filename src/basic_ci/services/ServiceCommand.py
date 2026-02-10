import subprocess
from pathlib import Path

from basic_ci import get_os


class ServiceCommand:
    """
    This service runs a custom command in the folder we're in.
    IN: command (list of str) to run, path (Path)
    OUT: CompletedProcess object with args, returncode, stdout, stderr
    """

    def run_command(self, command: list[str], path: Path):
        my_os = get_os.get_os_type()
        os_prefix = get_os.get_terminal_os_command(my_os)
        os_command = os_prefix + command
        
        output = subprocess.run(
            os_command,
            cwd=str(path),        
            capture_output=True,  
            text=True,
            check=False
        )
        return output
        