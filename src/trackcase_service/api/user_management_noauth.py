from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.user_management import (
    get_user_management_service,
    get_user_password_service,
)

router = APIRouter(
    prefix="/trackcase-service/users/na",
    tags=["User Management"],
)


@router.post(
    "/create/",
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
    "/login/",
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


@router.post(
    "/validate/",
    response_model=schemas.AppUserLoginResponse,
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
def validate_app_user(
    request: Request,
    email: str,
    db_session: Session = Depends(get_db_session),
):
    return get_user_password_service(
        plain_password=None, user_name=email
    ).validate_user(request, db_session)
