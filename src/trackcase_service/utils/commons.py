import http
import logging
import secrets

from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.db.session import get_db_session

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
    get_db_session()
    log.info("Created DB Session...")


def shutdown_db_client(app: FastAPI):
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
            msg="Invalid Credentials",
            err_msg="Basic Credentials",
        )
    # also check if user_name present in request headers or not
    # username header is sent from authenv_gateway after validation
    user_name = request.headers.get("usernameheader")
    if not is_ignore_username and not user_name:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            msg="Missing Username",
            err_msg="Missing Username",
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


def copy_objects(
    source_object, destination_class, destination_object=None, is_copy_all=False
):
    if destination_object is None:
        destination_object = destination_class()
    common_attributes = set(dir(source_object)) & set(dir(destination_object))
    for attr in common_attributes:
        if (
            not callable(getattr(source_object, attr))
            and not attr.startswith("_")
            and (is_copy_all or not getattr(destination_object, attr))
        ):
            setattr(destination_object, attr, getattr(source_object, attr))
    return destination_object
