import http
import logging
import secrets

from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import text
from sqlalchemy.orm import Session

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
            error="Invalid Credentials",
        )
    # also check if user_name present in request headers or not
    # username header is sent from authenv_gateway after validation
    user_name = request.headers.get("x-user-name")
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


def test_database(db_session: Session):
    test_database_sql = text("SELECT * FROM ZEST_TABLE")
    result = db_session.execute(test_database_sql)
    result_rows = result.fetchall()
    log.info(result_rows)


def reorg_tables(db_session: Session):
    check_reorg_sql = text(
        "SELECT TABSCHEMA, TABNAME FROM "
        "SYSIBMADM.ADMINTABINFO WHERE REORG_PENDING = 'Y'"
    )
    result = db_session.execute(check_reorg_sql)
    result_rows = result.fetchall()

    reorg_sqls = []
    for row in result_rows:
        reorg_sqls.append(
            text(f"""CALL SYSPROC.ADMIN_CMD('REORG TABLE "{row[0]}"."{row[1]}"')""")
        )

    for reorg_sql in reorg_sqls:
        db_session.execute(reorg_sql)


def get_err_msg(msg: str, err_msg: str = ""):
    return msg + "\n" + err_msg
