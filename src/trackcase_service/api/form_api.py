from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.form_service import get_form_service
from src.trackcase_service.service.schemas import FormRequest, FormResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/forms", tags=["Forms"])


@router.get("/", response_model=FormResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service(db_session).read_all_forms(request, is_include_extras)


@router.get("/{form_id}", response_model=FormResponse, status_code=HTTPStatus.OK)
def find_one(
    form_id: int,
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    form_response: FormResponse = get_form_service(db_session).read_one_form(
        form_id, request, is_include_extras
    )
    if form_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"Form Not Found By Id: {form_id}!!!",
        )
    return form_response


@router.post("/", response_model=FormResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    form_request: FormRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service(db_session).create_one_form(request, form_request)


@router.delete("/{form_id}", response_model=FormResponse, status_code=HTTPStatus.OK)
def delete_one(
    form_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service(db_session).delete_one_form(form_id, request)


@router.put("/{form_id}", response_model=FormResponse, status_code=HTTPStatus.OK)
def update_one(
    form_id: int,
    request: Request,
    form_request: FormRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service(db_session).update_one_form(form_id, request, form_request)
