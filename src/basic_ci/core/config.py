from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Holds basic information needed to run the CI service and to ensure that only the correct repos can be executed by the server.
    """
    
    GITHUB_WEBHOOK_SECRET: str
    PIPELINE_CONFIG_PATH: str
    GITHUB_TOKEN:str
    REPO_URL:str
    SAVE_FOLDER: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings(env_filename: str = ".env") -> Settings:
    """
    Gets the settings information from a file.
    
    Args:
        env_filename(str): Name of file with config details
        
    Returns:
        (Settings): Object with config information needed for the CI server to run.
    """
    
    return Settings(_env_file=env_filename)