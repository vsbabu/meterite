from typing import Dict
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Base settings. Use a .env file at the root to override.
    Api tokens are a dictionary - keep it in env as a json.
    See https://pypi.org/project/python-dotenv/
    """

    database_url: str = Field(default="sqlite:////tmp/testit.db", env="database_url")
    api_key_name: str = Field(default="x-auth-token", env="api_key_name")
    cookie_domain: str = Field(default="localtest.me", env="cookie_domain")
    api_tokens: Dict[str, str] = {"123456": "org_01", "567890": "org_02"}

    class Config:
        env_file = ".env"
        fields = {"api_tokens": {"env": "api_tokens"}}


# ---------- logging  ---------------------------------
from loguru import logger
