from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    """
    Configuration settings for API-AutotestMCP.
    Uses environment variables with API_TEST_ prefix.
    """
    model_config = SettingsConfigDict(
        env_prefix="API_TEST_",
        env_file=".env",
        extra="ignore"
    )

    # Directory where test reports are saved
    exports_dir: str = Field(default="exports")
    
    # Directory for client profiles (reserved for future use)
    profiles_dir: str = Field(default="profiles")
    
    # Log level (DEBUG, INFO, WARNING, ERROR)
    log_level: str = Field(default="INFO")

    @property
    def resolved_exports_dir(self) -> str:
        """Resolves ${workspaceFolder} to current working directory."""
        path = self.exports_dir
        if "${workspaceFolder}" in path:
            return path.replace("${workspaceFolder}", os.getcwd())
        return os.path.abspath(path)

    @property
    def resolved_profiles_dir(self) -> str:
        """Resolves ${workspaceFolder} to current working directory."""
        path = self.profiles_dir
        if "${workspaceFolder}" in path:
            return path.replace("${workspaceFolder}", os.getcwd())
        return os.path.abspath(path)

# Singleton instance
settings = Settings()
