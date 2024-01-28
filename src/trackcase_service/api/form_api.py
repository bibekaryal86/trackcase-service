from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

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
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service().read_all_forms(
        request, is_include_extra, is_include_history
    )


@router.get("/{form_id}/", response_model=FormResponse, status_code=HTTPStatus.OK)
def find_one(
    form_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    form_response: FormResponse = get_form_service().read_one_form(
        form_id,
        request,
        is_include_extra,
        is_include_history,
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
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service().create_one_form(request, form_request)


@router.delete("/{form_id}/", response_model=FormResponse, status_code=HTTPStatus.OK)
def delete_one(
    form_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service().delete_one_form(form_id, request)


@router.put("/{form_id}/", response_model=FormResponse, status_code=HTTPStatus.OK)
def update_one(
    form_id: int,
    request: Request,
    form_request: FormRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_service().update_one_form(form_id, request, form_request)
