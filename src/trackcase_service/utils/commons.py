import datetime
import http
import json
import logging
import os
import sys
from typing import Optional

import jwt
from fastapi import HTTPException, Query, Request
from fastapi.security import HTTPAuthorizationCredentials
from jwt import PyJWTError
from pydantic import ValidationError

import src.trackcase_service.service.schemas as schemas
import src.trackcase_service.utils.constants as constants
import src.trackcase_service.utils.logger as logger

log = logger.Logger(logging.getLogger(__name__))


def is_production():
    return constants.APP_ENV == "production"


def validate_input():
    missing_variables = []

    if constants.APP_ENV is None:
        missing_variables.append("APP_ENV")
    if constants.BASIC_AUTH_USR is None:
        missing_variables.append("BASIC_AUTH_USR")
    if constants.BASIC_AUTH_PWD is None:
        missing_variables.append("BASIC_AUTH_PWD")
    if constants.DB_USERNAME is None:
        missing_variables.append("DB_USERNAME")
    if constants.DB_PASSWORD is None:
        missing_variables.append("DB_PASSWORD")
    if constants.DB_NAME is None:
        missing_variables.append("DB_NAME")
    if constants.REPO_HOME is None:
        missing_variables.append("REPO_HOME")
    if constants.SECRET_KEY is None:
        missing_variables.append("SECRET_KEY")
    if constants.CORS_ORIGINS is None or len(constants.CORS_ORIGINS) == 0:
        missing_variables.append("CORS_ORIGINS")
    if constants.MJ_PUBLIC is None:
        missing_variables.append("MJ_PUBLIC")
    if constants.MJ_PRIVATE is None:
        missing_variables.append("MJ_PRIVATE")
    if constants.MJ_EMAIL is None:
        missing_variables.append("MJ_EMAIL")

    if len(missing_variables) != 0:
        raise ValueError(
            "The following env variables are missing: {}".format(missing_variables)
        )


def startup_app():
    log.info("App Starting...")


def shutdown_app():
    log.info("App Shutting Down...")


def get_err_msg(msg: str, err_msg: str = ""):
    return msg + "\n" + err_msg


def get_auth_user_token(request: Request) -> dict:
    return request.state.user_details


def set_auth_user_token(request: Request, app_user_token: dict):
    request.state.user_details = app_user_token


def raise_http_exception(
    request: Request,
    sts_code: http.HTTPStatus | int,
    error: str = "",
    exc_info=None,
):
    log.error(
        "HTTPException: [ {} ] | Status: [ {} ]".format(request.url, sts_code),
        extra=error,
        exc_info=exc_info,
    )
    raise HTTPException(status_code=sts_code, detail={"error": error})


def check_active_courts(courts: list[schemas.Court]) -> bool:
    active_statuses = constants.get_statuses().get("court").get("active")
    for court in courts:
        if court.status in active_statuses:
            return True
    return False


def check_active_judges(judges: list[schemas.Judge]) -> bool:
    active_statuses = constants.get_statuses().get("judge").get("active")
    for judge in judges:
        if judge.status in active_statuses:
            return True
    return False


def check_active_clients(clients: list[schemas.Client]) -> bool:
    active_statuses = constants.get_statuses().get("client").get("active")
    for client in clients:
        if client.status in active_statuses:
            return True
    return False


def check_active_court_cases(court_cases: list[schemas.CourtCase]) -> bool:
    active_statuses = constants.get_statuses().get("court_case").get("active")
    for court_case in court_cases:
        if court_case.status in active_statuses:
            return True
    return False


def check_active_hearing_calendars(
    hearing_calendars: list[schemas.HearingCalendar],
) -> bool:
    active_statuses = constants.get_statuses().get("calendars").get("active")
    for hearing_calendar in hearing_calendars:
        if hearing_calendar.status in active_statuses:
            return True
    return False


def check_active_task_calendars(task_calendars: list[schemas.TaskCalendar]) -> bool:
    active_statuses = constants.get_statuses().get("calendars").get("active")
    for task_calendar in task_calendars:
        if task_calendar.status in active_statuses:
            return True
    return False


def check_active_forms(forms: list[schemas.Filing]) -> bool:
    active_statuses = constants.get_statuses().get("form").get("active")
    for form in forms:
        if form.status in active_statuses:
            return True
    return False


def check_active_case_collections(
    case_collections: list[schemas.CaseCollection],
) -> bool:
    active_statuses = constants.get_statuses().get("collections").get("active")
    for case_collection in case_collections:
        if case_collection.status in active_statuses:
            return True
    return False


def check_active_cash_collections(
    cash_collections: list[schemas.CashCollection],
) -> bool:
    active_statuses = constants.get_statuses().get("collections").get("active")
    for cash_collection in cash_collections:
        if cash_collection.status in active_statuses:
            return True
    return False


def request_metadata_example() -> str:
    return """For example -:-:- {
    "request_object_id": 1,
    "sort_config": {
        "column": "full_name",
        "direction": "asc"
    },
    "filter_config": [
        {
            "column": "full_name",
            "value": "some name",
            "operation": "eq"
        },
        {
            "column": "email",
            "value": "column@value.com",
            "operation": "eq"
        }
    ],
    "page_number": 1,
    "per_page": 100,
    "is_include_deleted": false
}"""


def parse_request_metadata(
    request: Request,
    metadata: Optional[str] = Query(
        default=None, description=request_metadata_example()
    ),
) -> schemas.RequestMetadata:
    if metadata is None:
        return schemas.RequestMetadata()
    try:
        metadata_dict = json.loads(metadata)
        return schemas.RequestMetadata(**metadata_dict)
    except (json.JSONDecodeError, ValidationError) as ex:
        raise_http_exception(
            request,
            http.HTTPStatus.BAD_REQUEST,
            get_err_msg("Invalid Request Metadata JSON", str(ex)),
            exc_info=sys.exc_info(),
        )


def encode_auth_credentials(app_user: schemas.AppUser):
    token_claim = {
        "app_user_token": app_user.to_token(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(payload=token_claim, key=constants.SECRET_KEY, algorithm="HS256")


def encode_email_address(email: str, minutes: int):
    token_claim = {
        "email_token": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes),
    }
    return jwt.encode(payload=token_claim, key=constants.SECRET_KEY, algorithm="HS256")


def decode_email_address(
    request: Request,
    encoded_email: str,
):
    try:
        token_claims = jwt.decode(
            jwt=encoded_email,
            key=constants.SECRET_KEY,
            algorithms=["HS256"],
        )

        email_token_claim = token_claims.get("email_token")

        if email_token_claim:
            return email_token_claim

        raise_http_exception(
            request,
            http.HTTPStatus.FORBIDDEN,
            error="Incorrect Email Credentials",
        )
    except PyJWTError as ex:
        raise_http_exception(
            request,
            http.HTTPStatus.BAD_REQUEST,
            get_err_msg("Invalid Email Credentials", str(ex)),
            exc_info=sys.exc_info(),
        )


def decode_auth_credentials(
    request: Request,
    http_auth_credentials: HTTPAuthorizationCredentials,
):
    try:
        token_claims = jwt.decode(
            jwt=http_auth_credentials.credentials,
            key=constants.SECRET_KEY,
            algorithms=["HS256"],
        )

        app_user_token = token_claims.get("app_user_token")

        if app_user_token:
            set_auth_user_token(request, app_user_token)
        else:
            raise_http_exception(
                request,
                http.HTTPStatus.UNAUTHORIZED,
                error="Incorrect Credentials",
            )
    except PyJWTError as ex:
        raise_http_exception(
            request,
            http.HTTPStatus.BAD_REQUEST,
            get_err_msg("Invalid Credentials", str(ex)),
            exc_info=sys.exc_info(),
        )


def read_file(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, "r") as file:
        content = file.read()
    return content
