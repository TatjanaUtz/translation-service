"""Config.

This module contains the configuration settings for the translation service application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):  # type: ignore[misc]
    """Configuration settings for the translation service application."""

    source_languages: list[str] = ["de", "en", "es", "fr", "it", "ja", "ko", "pl", "ru", "sk", "tr", "zh"]
    target_languages: list[str] = ["de", "en", "es", "fr", "it"]

    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
