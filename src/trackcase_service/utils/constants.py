import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# Constants
ENV_APP_PORT = "APP_PORT"

STANDARD_USER_ROLE_ID = 3
TASK_ID_DUE_AT_HEARING = 1
DEFAULT_HEARING_TO_TASK_CALENDAR_DATE = 15
HEARING_TO_TASK_CALENDAR_DATE: dict[str, int] = {
    "MASTER": 30,
    "MERIT": 15,
}
TRACKCASE_UI_HOME_PROD = "https://trackcase.appspot.com"
TRACKCASE_UI_HOME_DEV = "http://10.0.0.73:9191"


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
DB_NAME = get_settings().db_name
REPO_HOME = get_settings().repo_home
SECRET_KEY = get_settings().secret_key
CORS_ORIGINS = get_settings().cors_origins
MJ_PUBLIC = get_settings().mj_public
MJ_PRIVATE = get_settings().mj_private
MJ_EMAIL = get_settings().mj_email
