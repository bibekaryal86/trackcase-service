import http
import logging
import secrets

from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBasicCredentials

from . import constants, logger

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

    if len(missing_variables) != 0:
        raise ValueError(
            "The following env variables are missing: {}".format(missing_variables)
        )


def startup_db_client(app: FastAPI):
    log.info("App Starting...")


def shutdown_db_client(app: FastAPI):
    log.info("App Shutting Down...")


def validate_http_basic_credentials(
    request: Request, http_basic_credentials: HTTPBasicCredentials
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
            msg="Invalid Credentials",
            err_msg="Basic Credentials",
        )


def raise_http_exception(
    request: Request,
    sts_code: http.HTTPStatus | int,
    msg: str = "",
    err_msg: str = "",
    detail=None,
):
    log.error(
        "ERROR:::HTTPException: [ {} ] | Status: [ {} ]".format(request.url, sts_code),
    )
    if detail is None:
        raise HTTPException(
            status_code=sts_code, detail={"msg": msg, "errMsg": err_msg}
        )
    else:
        raise HTTPException(status_code=sts_code, detail=detail)
