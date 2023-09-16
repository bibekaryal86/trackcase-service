import os
from functools import lru_cache

from fastapi.security import HTTPBasic
from pydantic_settings import BaseSettings, SettingsConfigDict


# Constants
ENV_APP_PORT = "APP_PORT"
http_basic_security = HTTPBasic()


# ENVIRONMENT VARIABLES
class Settings(BaseSettings):
    if os.getenv("IS_PYTEST"):
        model_config = SettingsConfigDict(env_file=".env.example", extra="allow")
    else:
        model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_settings():
    return Settings()


APP_ENV = get_settings().app_env
BASIC_AUTH_USR = get_settings().basic_auth_usr
BASIC_AUTH_PWD = get_settings().basic_auth_pwd
