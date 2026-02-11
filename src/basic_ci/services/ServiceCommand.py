import subprocess
from pathlib import Path


class ServiceCommand:
    """
    This service runs a custom command in the folder we're in.
    IN: command (list of str) to run, path (Path)
    OUT: CompletedProcess object with args, returncode, stdout, stderr
    """

    def run_command(self, command: list[str], path: Path) -> subprocess.CompletedProcess:
        command_str = " ".join(command) # To make command format compatible with shell=True 
        
        output = subprocess.run(
            command_str,
            cwd=str(path),        
            capture_output=True,  
            text=True,
            check=False,
            shell=True, # subprocess will get the correct shell for the correct OS, making get_OS redundant
        )
        return output
        