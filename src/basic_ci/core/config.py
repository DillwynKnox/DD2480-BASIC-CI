from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GITHUB_WEBHOOK_SECRET: str
    PIPELINE_CONFIG_PATH: str
    GITHUB_TOKEN:str
    REPO_URL:str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings(env_filename: str = ".env") -> Settings:
    """_env_file is a valid parameter inherited from BaseSettings, but it's excluded
    from public type stubs (leading underscore). This tells mypy to ignore the
    false positive "unexpected argument" error."""
    return Settings(_env_file=env_filename) # type: ignore[call-arg]