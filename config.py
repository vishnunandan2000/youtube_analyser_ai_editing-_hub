"""
Application Configuration for GenAI Video Intelligence Studio.
Manages environment variables, default paths, and system parameters.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os
import shutil

# Root project directory
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # Ollama settings
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.2:latest", alias="OLLAMA_MODEL")
    ollama_timeout_seconds: int = Field(default=90, alias="OLLAMA_TIMEOUT_SECONDS")

    # YouTube API settings
    youtube_api_key: str = Field(default="", alias="YOUTUBE_API_KEY")
    youtube_client_secrets_file: str = Field(default="", alias="YOUTUBE_CLIENT_SECRETS_FILE")

    # Storage and Job Management
    database_url: str = Field(default="sqlite:///data/app.db", alias="DATABASE_URL")
    max_upload_size_mb: int = Field(default=500, alias="MAX_UPLOAD_SIZE_MB")
    max_video_duration_minutes: int = Field(default=60, alias="MAX_VIDEO_DURATION_MINUTES")
    max_concurrent_jobs: int = Field(default=1, alias="MAX_CONCURRENT_JOBS")
    default_output_language: str = Field(default="en", alias="DEFAULT_OUTPUT_LANGUAGE")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # Directory Paths
    base_dir: Path = BASE_DIR
    data_dir: Path = BASE_DIR / "data"
    jobs_dir: Path = BASE_DIR / "data" / "jobs"
    exports_dir: Path = BASE_DIR / "data" / "exports"
    cache_dir: Path = BASE_DIR / "data" / "cache"
    assets_dir: Path = BASE_DIR / "assets"
    fonts_dir: Path = BASE_DIR / "assets" / "fonts"
    overlays_dir: Path = BASE_DIR / "assets" / "overlays"
    templates_dir: Path = BASE_DIR / "assets" / "templates"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def init_directories(self) -> None:
        """Ensure all required runtime directories exist."""
        for path in [
            self.data_dir,
            self.jobs_dir,
            self.exports_dir,
            self.cache_dir,
            self.assets_dir,
            self.fonts_dir,
            self.overlays_dir,
            self.templates_dir
        ]:
            path.mkdir(parents=True, exist_ok=True)

# Global settings singleton
settings = Settings()
settings.init_directories()
