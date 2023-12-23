import os
from enum import Enum
from functools import lru_cache

from fastapi.security import HTTPBasic
from pydantic_settings import BaseSettings, SettingsConfigDict

# Constants
ENV_APP_PORT = "APP_PORT"
http_basic_security = HTTPBasic()
USERNAME_HEADER = "x-user-name"


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
DB_USERNAME = get_settings().db_username
DB_PASSWORD = get_settings().db_password
REPO_HOME = get_settings().repo_home


class LogLevelOptions(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


@lru_cache()
def get_statuses():
    return {
        "court": ["ACTIVE", "INACTIVE", "CLOSED"],
        "judge": ["ACTIVE", "INACTIVE", "CLOSED"],
        "client": ["ACTIVE", "COMPLETED", "TRANSFERRED", "CLOSED"],
        "court_case": ["OPEN", "CLOSED"],
        "hearing_calendar": ["OPEN", "PROCESSING", "CLOSED"],
        "task_calendar": ["OPEN", "PROCESSING", "CLOSED"],
        "form": [
            "OPEN",
            "PROCESSING",
            "PENDING",
            "SUBMITTED",
            "EVIDENCE",
            "APPROVED",
            "DENIED",
            "WITHDRAWN",
            "CLOSED",
        ],
        "case_collection": ["OPEN", "PENDING", "CLOSED"],
        "cash_collection": ["PENDING", "RECEIVED", "WAIVED", "CLOSED"],
    }
