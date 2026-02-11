from pathlib import Path
from typing import List

from basic_ci.schemes.pipeline import Stage
from basic_ci.schemes.stage_result import Stage_result
from basic_ci.services import pipeline_config_service
from basic_ci.services.pipeline_config_service import Pipeline_Config_service
from basic_ci.services.ServiceCommand import ServiceCommand


class Pipeline_stage_service:
    def __init__(self,command_service:ServiceCommand,pipeline_config_service:Pipeline_Config_service = pipeline_config_service):
        self.command_service = command_service
        self.pipeline_config_service = pipeline_config_service

    def run_stage(self,stage: Stage, path:str | Path)->Stage_result:
        """
        This runs a stage in the pipeline, which is a command.
        """
        result = self.command_service.run_command(stage.command.split(), path=Path(path))
        return Stage_result(
            name=stage.stage,
            success=result.returncode == 0,
            command=stage.command,
            output=result.stdout + result.stderr
        )
    
    def run_stages(self,path:str | Path) -> List[Stage_result]:
        """
        This gets the stages from the pipeline and runs them.
        """
        stages = self.pipeline_config_service.get_pipeline().stages
        results = []
        for stage in stages:
            result = self.run_stage(stage, path=path)
            results.append(result)
        return results
