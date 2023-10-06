from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.history_form_service import get_history_form_service
from src.trackcase_service.service.schemas import (
    HistoryFormRequest,
    HistoryFormResponse,
)
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/history_forms", tags=["HistoryForms"])


@router.get("/", response_model=HistoryFormResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_history_form_service(db_session).read_all_history_forms(
        request, is_include_extras
    )


@router.get(
    "/{history_form_id}", response_model=HistoryFormResponse, status_code=HTTPStatus.OK
)
def find_one(
    history_form_id: int,
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    history_form_response: HistoryFormResponse = get_history_form_service(
        db_session
    ).read_one_history_form(history_form_id, request, is_include_extras)
    if history_form_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"HistoryForm Not Found By Id: {history_form_id}!!!",
        )
    return history_form_response


@router.get(
    "/form/{form_id}", response_model=HistoryFormResponse, status_code=HTTPStatus.OK
)
def find_many(
    form_id: int,
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_history_form_service(db_session).read_many_history_forms_by_form_id(
        form_id, request, is_include_extras
    )


@router.post("/", response_model=HistoryFormResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    history_form_request: HistoryFormRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_history_form_service(db_session).create_one_history_form(
        request, history_form_request
    )


@router.delete(
    "/{history_form_id}", response_model=HistoryFormResponse, status_code=HTTPStatus.OK
)
def delete_one(
    history_form_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_history_form_service(db_session).delete_one_history_form(
        history_form_id, request
    )


@router.put(
    "/{history_form_id}", response_model=HistoryFormResponse, status_code=HTTPStatus.OK
)
def update_one(
    history_form_id: int,
    request: Request,
    history_form_request: HistoryFormRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_history_form_service(db_session).update_one_history_form(
        history_form_id, request, history_form_request
    )
