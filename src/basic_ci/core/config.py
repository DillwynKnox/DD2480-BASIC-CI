from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GITHUB_WEBHOOK_SECRET: str
    PIPELINE_CONFIG_PATH: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings(env_filename: str = ".env") -> Settings:
    return Settings(_env_file=env_filename)