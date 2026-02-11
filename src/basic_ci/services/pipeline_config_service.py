
import yaml

from basic_ci.core.config import Settings, get_settings
from basic_ci.schemes.pipeline import PipelineConfig, Stage


class Pipeline_Config_service:
    def __init__(self,settings:Settings = get_settings()):
        """
        Service to read the configuration of the pipeline.

        Args:
            settings (Settings object): containing the configuration.
    
        """
        
        self.settings = settings
    
    def load_pipeline_config(self) -> PipelineConfig:
        """
        Loads the pipeline configuration from a YAML file specified in the settings.
        
        Returns:
            config (PipelineConfig object): containing information about the project and the stages.
            
        Raises:
            FileNotFoundError: If pipelin configuration file cannot be found.
            ValueError: If pipeline configuration cannot be parsed.
        """
        try:
            with open(self.settings.PIPELINE_CONFIG_PATH, "r") as f:
                raw_data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Pipeline configuration file not found at {self.settings.PIPELINE_CONFIG_PATH}")

        try:
            config = PipelineConfig(
                project=raw_data.get('project', 'default_project'),
                stages=[Stage(**s) for s in raw_data.get('stages', [])]
            )    
        except Exception as e:
            raise ValueError(f"Error parsing pipeline configuration: {e}") 
        return config
    

def get_pipeline_config_service() -> Pipeline_Config_service:
    """
    Factory function to create a Pipeline_Config_service instance.
    """
    return Pipeline_Config_service(settings=get_settings())
        