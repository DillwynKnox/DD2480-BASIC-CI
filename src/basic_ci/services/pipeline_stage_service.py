from pathlib import Path
from typing import List

from basic_ci.schemes.pipeline import Stage
from basic_ci.schemes.stage_result import Stage_result
from basic_ci.services import pipeline_config_service
from basic_ci.services.pipeline_config_service import Pipeline_Config_service
from basic_ci.services.ServiceCommand import ServiceCommand


class Pipeline_stage_service:
    def __init__(self,command_service:ServiceCommand,pipeline_config_service:Pipeline_Config_service = pipeline_config_service):
        """
        Setup in order to be able to execute stages of pipeline

        Args:
            command_service (ServiceCommand): Object used to run commands.
            pipeline_config_service (Pipeline_Config_service): Object that hold pipeline configuration
        """
            
        self.command_service = command_service
        self.pipeline_config_service = pipeline_config_service

 
    def run_stage(self,stage: Stage, path:str)->Stage_result:
        """
        This runs a stage in the pipeline, which is a command.
        
        Args:
            stage(Stage): Holds information about commands to execute during this stage.
            path(str): Path of the directory where command is run.
        Returns:
            (Stage_result): Information about the execution of this stage.
        
        """
        result = self.command_service.run_command(stage.command.split(), path=Path(path))
        return Stage_result(
            name=stage.stage,
            success=result.returncode == 0,
            command=stage.command,
            output=result.stdout + result.stderr
        )
    
    def run_stages(self,path:str) -> List[Stage_result]:
        """
        This gets the stages from the pipeline and runs them by calling .run_stage().
        
        Args:
            path(str): The path of the directory.
        
        Returns:
            List of stage_results: Information from execution of each stage.
        """
        stages = self.pipeline_config_service.get_pipeline().stages
        results = []
        for stage in stages:
            result = self.run_stage(stage, path=path)
            results.append(result)
        return results
