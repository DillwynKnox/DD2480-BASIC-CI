import subprocess
from pathlib import Path


class ServiceCommand:


    def run_command(self, command: list[str], path: Path) -> subprocess.CompletedProcess:
        """
        This service runs a custom command in the folder we're in. It runs them in a shell.

        Args:
            command (list of str): Commands to run.
            path (Path): path to directory where commands are run from

        Returns:
            CompletedProcess object: Contains args, returncode, stdout, stderr
        """
        
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
    
def get_ServiceCommand()->ServiceCommand:
    """
    Factury for ServiceCommnads    
    :return: returns a new instance of ServiceCommand
    :rtype: ServiceCommand
    """
    return ServiceCommand()