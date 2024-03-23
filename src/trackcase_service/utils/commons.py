import datetime
import http
import json
import logging
import os
import sys
from functools import wraps
from typing import List, Optional

import jwt
from fastapi import HTTPException, Query, Request
from fastapi.security import HTTPAuthorizationCredentials
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

import src.trackcase_service.service.schemas as schemas
import src.trackcase_service.utils.constants as constants
import src.trackcase_service.utils.logger as logger
from src.trackcase_service.db.crud import DataKeys
from src.trackcase_service.db.session import SessionLocal

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


async def startup_app():
    log.info("App Starting...")
    # initialize caches
    await initialize_caches()


def shutdown_app():
    log.info("App Shutting Down...")


async def initialize_caches():
    from src.trackcase_service.service.ref_types import get_ref_types_service
    from src.trackcase_service.service.user_management import (
        get_user_management_service,
    )

    request = Request(scope={"type": "http"})
    request.state.user_details = {"roles": [{"name": "SUPERUSER"}]}
    db_session: Session = SessionLocal()

    get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).get_component_status(
        request=request, component_name=schemas.ComponentStatusNames.APP_USER
    )
    get_ref_types_service(
        schemas.RefTypesServiceRegistry.COLLECTION_METHOD, db_session
    ).get_collection_method(request)
    get_ref_types_service(
        schemas.RefTypesServiceRegistry.CASE_TYPE, db_session
    ).get_case_type(request)
    get_ref_types_service(
        schemas.RefTypesServiceRegistry.FILING_TYPE, db_session
    ).get_filing_type(request)
    get_ref_types_service(
        schemas.RefTypesServiceRegistry.HEARING_TYPE, db_session
    ).get_hearing_type(request)
    get_ref_types_service(
        schemas.RefTypesServiceRegistry.TASK_TYPE, db_session
    ).get_task_type(request)
    get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE, db_session
    ).get_app_role(request)
    get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_PERMISSION, db_session
    ).get_app_permission(request)
    db_session.close()
    await request.close()


# def reset_caches():
#     from src.trackcase_service.utils import cache
#     cache.COMPONENT_STATUSES_CACHE.clear()
#     cache.COLLECTION_METHODS_CACHE.clear()
#     cache.CASE_TYPES_CACHE.clear()
#     cache.FILING_TYPES_CACHE.clear()
#     cache.HEARING_TYPES_CACHE.clear()
#     cache.TASK_TYPES_CACHE.clear()
#     cache.APP_ROLES_CACHE.clear()
#     cache.APP_PERMISSIONS_CACHE.clear()


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


def request_metadata_example() -> str:
    return """For example -:-:- {
    "request_object_id": 1,
    "sort_config": {
        "column": "full_name",
        "direction": "ASC"
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
    "is_include_deleted": false,
    "is_include_extra": false,
    "is_include_history": false
}"""


def parse_request_metadata(
    request: Request,
    metadata: Optional[str] = Query(
        default=None, description=request_metadata_example()
    ),
) -> schemas.RequestMetadata | None:
    if metadata is None:
        return None
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


def has_permission(permission_name: str, request: Request):
    user_details = getattr(request.state, "user_details", None)
    if user_details is None:
        return False

    for role in user_details.get("roles", []):
        if role.get("name") == "SUPERUSER":
            return True
        else:
            permissions = role.get("permissions", [])
            for permission in permissions:
                if permission.get("name") == permission_name:
                    return True

    return False


def check_permissions(permission_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                raise_http_exception(
                    request=Request(scope={"type": "http"}),
                    sts_code=http.HTTPStatus.FORBIDDEN,
                    error="Request object not found...",
                )
            if not has_permission(permission_name, request):
                raise_http_exception(
                    request=request,
                    sts_code=http.HTTPStatus.FORBIDDEN,
                    error="Insufficient permissions...",
                )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def read_file(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, "r") as file:
        content = file.read()
    return content


def get_read_response_data_metadata(read_response):
    if read_response:
        return read_response.get(DataKeys.data) or [], read_response.get(
            DataKeys.metadata
        )
    return [], None


def check_active_component_status(components: list, active_statuses: list[int]) -> bool:
    for component in components:
        if component.component_status_id in active_statuses:
            return True
    return False


def get_sort_config_raw(sort_config: schemas.SortConfig = None) -> str:
    if sort_config and sort_config.column and sort_config.direction:
        sort_table = sort_config.table
        sort_column = sort_config.column
        sort_direction = sort_config.direction.value
        if sort_table:
            return f" ORDER BY {sort_table}.{sort_column} {sort_direction}"
        else:
            return f" ORDER BY {sort_column} {sort_direction}"
    return ""


def get_filter_config_raw(filter_config: List[schemas.FilterConfig]) -> str:
    filter_clauses = []
    for filter_item in filter_config:
        table = filter_item.table
        column = filter_item.column
        value = filter_item.value
        operation = filter_item.operation
        if isinstance(value, str):
            value = f"'{value}'"
        elif isinstance(value, datetime.datetime):
            value = f"'{value.isoformat()}'"
        if table:
            filter_clauses.append(
                f"{table}.{column} {get_operation_symbol(operation)} {value}"
            )
        else:
            filter_clauses.append(f"{column} {get_operation_symbol(operation)} {value}")
    return " AND ".join(filter_clauses)


def get_operation_symbol(operation: schemas.FilterOperation) -> str:
    operation_symbols = {
        schemas.FilterOperation.EQUAL_TO: "=",
        schemas.FilterOperation.GREATER_THAN: ">",
        schemas.FilterOperation.LESS_THAN: "<",
        schemas.FilterOperation.GREATER_THAN_OR_EQUAL_TO: ">=",
        schemas.FilterOperation.LESS_THAN_OR_EQUAL_TO: "<=",
    }
    return operation_symbols[operation]
