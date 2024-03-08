from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.user_management import (
    get_user_management_service,
    get_user_password_service,
)
from src.trackcase_service.utils.commons import is_production
from src.trackcase_service.utils.constants import (
    TRACKCASE_UI_HOME_DEV,
    TRACKCASE_UI_HOME_PROD,
)
from src.trackcase_service.utils.email import get_email_service

router = APIRouter(
    prefix="/users/na",
    tags=["User Management"],
)


@router.post(
    "/app_users/create/",
    response_model=schemas.AppUserResponse,
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
def insert_app_user(
    request: Request,
    app_user_request: schemas.AppUserRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER, db_session
    ).create_app_user(request, app_user_request)


@router.post(
    "/app_users/login/",
    response_model=schemas.AppUserLoginResponse,
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
def login_app_user(
    request: Request,
    login_request: schemas.AppUserLoginRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_password_service(
        login_request.password, login_request.username
    ).login_user(request, db_session)


@router.get(
    "/app_users/validate_init/",
    include_in_schema=False,
)
def validate_app_user_init(
    request: Request,
    to_validate: str,
):
    get_email_service().app_user_validation_email(request, to_validate)
    return JSONResponse(content={})


@router.get(
    "/app_users/validate_exit/",
    include_in_schema=False,
)
def validate_app_user_exit(
    request: Request,
    to_validate: str,
    db_session: Session = Depends(get_db_session),
):
    url = _get_redirect_base_url()
    try:
        get_user_password_service(
            plain_password=None, user_name=to_validate
        ).validate_reset_user(request, db_session)
        url = f"{url}?is_validated=true"
    except Exception:
        url = f"{url}?is_validated=false"
    return RedirectResponse(url=url)


@router.get(
    "/app_users/reset_init/",
    include_in_schema=False,
)
def reset_app_user_init(
    request: Request,
    to_reset: str,
):
    get_email_service().app_user_reset_email(request, to_reset)
    return JSONResponse(content={})


@router.get(
    "/app_users/reset_mid/",
    include_in_schema=False,
)
def reset_app_user_mid(
    request: Request,
    to_reset: str,
    db_session: Session = Depends(get_db_session),
):
    url = _get_redirect_base_url()
    try:
        user_model_id = get_user_password_service(
            plain_password=None, user_name=to_reset
        ).validate_reset_user(request, db_session, False)
        url = f"{url}?is_reset=true&user_model_id={user_model_id}"
    except Exception as ex:
        url = f"{url}?is_reset=false"
    return RedirectResponse(url=url)


@router.get(
    "/app_users/reset_exit/",
    include_in_schema=False,
)
def reset_app_user_exit(
    request: Request,
    reset_request: schemas.AppUserLoginRequest,
    db_session: Session = Depends(get_db_session),
):
    get_user_password_service(
        plain_password=reset_request.password, user_name=reset_request.username
    ).reset_user_password(request, db_session)
    return JSONResponse(content={})


def _get_redirect_base_url():
    return TRACKCASE_UI_HOME_PROD if is_production() else TRACKCASE_UI_HOME_DEV
