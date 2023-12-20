from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.form_status_service import get_form_status_service
from src.trackcase_service.service.schemas import FormStatusRequest, FormStatusResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/form_statuses", tags=["FormStatuses"])


@router.get("/", response_model=FormStatusResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra_objects: bool = False,
    is_include_extra_lists: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_status_service(db_session).read_all_form_statuses(
        request, is_include_extra_objects, is_include_extra_lists, is_include_history
    )


@router.get(
    "/{form_status_id}", response_model=FormStatusResponse, status_code=HTTPStatus.OK
)
def find_one(
    form_status_id: int,
    request: Request,
    is_include_extra_objects: bool = False,
    is_include_extra_lists: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    form_status_response: FormStatusResponse = get_form_status_service(
        db_session
    ).read_one_form_status(
        form_status_id,
        request,
        is_include_extra_objects,
        is_include_extra_lists,
        is_include_history,
    )
    if form_status_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"FormStatus Not Found By Id: {form_status_id}!!!",
        )
    return form_status_response


@router.post("/", response_model=FormStatusResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    form_status_request: FormStatusRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_status_service(db_session).create_one_form_status(
        request, form_status_request
    )


@router.delete(
    "/{form_status_id}", response_model=FormStatusResponse, status_code=HTTPStatus.OK
)
def delete_one(
    form_status_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_status_service(db_session).delete_one_form_status(
        form_status_id, request
    )


@router.put(
    "/{form_status_id}", response_model=FormStatusResponse, status_code=HTTPStatus.OK
)
def update_one(
    form_status_id: int,
    request: Request,
    form_status_request: FormStatusRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_status_service(db_session).update_one_form_status(
        form_status_id, request, form_status_request
    )
