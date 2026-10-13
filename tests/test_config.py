"""
Unit tests for configuration and directory paths.
"""

from config import settings
from pathlib import Path

def test_settings_initialization():
    assert settings.ollama_base_url is not None
    assert "llama3.2" in settings.ollama_model
    assert settings.max_upload_size_mb > 0
    assert settings.max_concurrent_jobs >= 1

def test_directory_creation():
    settings.init_directories()
    assert settings.data_dir.exists()
    assert settings.jobs_dir.exists()
    assert settings.exports_dir.exists()
    assert settings.cache_dir.exists()
