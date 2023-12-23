import http
import logging
import secrets

from fastapi import HTTPException, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import text
from sqlalchemy.orm import Session

import src.trackcase_service.utils.constants as constants
import src.trackcase_service.utils.logger as logger
from src.trackcase_service.db.session import get_db_session

log = logger.Logger(logging.getLogger(__name__), __name__)


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
    test_database_sql = text("SELECT * FROM ZEST_TABLE")
    result = db_session.execute(test_database_sql)
    result_rows = result.fetchall()
    log.info(result_rows)


def get_err_msg(msg: str, err_msg: str = ""):
    return msg + "\n" + err_msg
