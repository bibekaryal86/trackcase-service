import os
from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# Constants
ENV_APP_PORT = "APP_PORT"
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
    category_statuses = {
        "court": {
            "active": ["ACTIVE"],
            "inactive": ["INACTIVE", "CLOSED"],
        },
        "judge": {
            "active": ["ACTIVE"],
            "inactive": ["INACTIVE", "CLOSED"],
        },
        "client": {
            "active": ["ACTIVE"],
            "inactive": ["COMPLETED", "TRANSFERRED", "CLOSED"],
        },
        "court_case": {
            "active": ["OPEN"],
            "inactive": ["CLOSED"],
        },
        "calendars": {
            "active": ["OPEN", "PROCESSING"],
            "inactive": ["COMPLETED", "CLOSED"],
        },
        "form": {
            "active": ["OPEN", "PROCESSING", "PENDING", "SUBMITTED", "EVIDENCE"],
            "inactive": [
                "APPROVED",
                "DENIED",
                "WITHDRAWN",
                "CLOSED",
            ],
        },
        "collections": {
            "active": ["OPEN", "PENDING"],
            "inactive": ["RECEIVED", "WAIVED", "COMPLETED", "CLOSED"],
        },
    }

    for category_status in category_statuses:
        category_statuses[category_status]["all"] = (
            category_statuses[category_status]["active"]
            + category_statuses[category_status]["inactive"]
        )

    return category_statuses


HEARING_TO_TASK_CALENDAR_DATE = {
    'MASTER': 30,
    'MERIT': 15,
    'DEFAULT': 15
}
