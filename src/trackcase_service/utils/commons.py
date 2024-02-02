import http
import logging
import secrets

from fastapi import HTTPException, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

import src.trackcase_service.service.schemas as schemas
import src.trackcase_service.utils.constants as constants
import src.trackcase_service.utils.logger as logger
from src.trackcase_service.db.session import get_db_session

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

    if constants.REPO_HOME is None:
        missing_variables.append("REPO_HOME")

    if len(missing_variables) != 0:
        raise ValueError(
            "The following env variables are missing: {}".format(missing_variables)
        )


def startup_db_client():
    log.info("App Starting...")
    get_db_session()
    log.info("Created DB Session...")


def shutdown_db_client():
    log.info("App Shutting Down...")


def validate_http_basic_credentials(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials,
    is_ignore_username: bool = False,
):
    valid_username = constants.BASIC_AUTH_USR
    valid_password = constants.BASIC_AUTH_PWD
    input_username = http_basic_credentials.username
    input_password = http_basic_credentials.password
    is_correct_username = secrets.compare_digest(
        valid_username.encode("utf-8"), input_username.encode("utf-8")
    )
    is_correct_password = secrets.compare_digest(
        valid_password.encode("utf-8"), input_password.encode("utf-8")
    )
    if not (is_correct_username and is_correct_password):
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.UNAUTHORIZED,
            error="Invalid Credentials",
        )

    # also check if user_name present in request headers or not
    user_name = request.headers.get(constants.USERNAME_HEADER)
    if not is_ignore_username and not user_name:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            error="Missing Username",
        )


def raise_http_exception(
    request: Request,
    sts_code: http.HTTPStatus | int,
    error: str = "",
):
    log.error(
        "ERROR:::HTTPException: [ {} ] | Status: [ {} ]".format(request.url, sts_code),
    )
    raise HTTPException(status_code=sts_code, detail={"error": error})


def test_database(db_session: Session):
    try:
        test_database_sql = text("SELECT TEST FROM ZEST_TABLE")
        result = db_session.execute(test_database_sql)
        result_row = result.fetchone()
        if result_row:
            return {"test_db_success": result_row[0]}
        else:
            return {"test_db": "maybe_success_but_no_data"}
    except OperationalError as ex:
        return {"test_db_failure": str(ex)}


def get_err_msg(msg: str, err_msg: str = ""):
    return msg + "\n" + err_msg


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
    active_statuses = constants.get_statuses().get("hearing_calendar").get("active")
    for hearing_calendar in hearing_calendars:
        if hearing_calendar.status in active_statuses:
            return True
    return False


def check_active_task_calendars(task_calendars: list[schemas.TaskCalendar]) -> bool:
    active_statuses = constants.get_statuses().get("task_calendar").get("active")
    for task_calendar in task_calendars:
        if task_calendar.status in active_statuses:
            return True
    return False


def check_active_forms(forms: list[schemas.Form]) -> bool:
    active_statuses = constants.get_statuses().get("form").get("active")
    for form in forms:
        if form.status in active_statuses:
            return True
    return False


def check_active_case_collections(
    case_collections: list[schemas.CaseCollection],
) -> bool:
    active_statuses = constants.get_statuses().get("case_collection").get("active")
    for case_collection in case_collections:
        if case_collection.status in active_statuses:
            return True
    return False


def check_active_cash_collections(
    cash_collections: list[schemas.CashCollection],
) -> bool:
    active_statuses = constants.get_statuses().get("cash_collection").get("active")
    for cash_collection in cash_collections:
        if cash_collection.status in active_statuses:
            return True
    return False
