from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.service.form_type_service import get_form_type_service
from src.trackcase_service.service.schemas import FormTypeRequest, FormTypeResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/form_types", tags=["FormTypes"])


@router.get("/", response_model=FormTypeResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_type_service().read_all_form_types(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{form_type_id}/", response_model=FormTypeResponse, status_code=HTTPStatus.OK
)
def find_one(
    form_type_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    form_type_response: FormTypeResponse = get_form_type_service().read_one_form_type(
        form_type_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if form_type_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"FormType Not Found By Id: {form_type_id}!!!",
        )
    return form_type_response


@router.post("/", response_model=FormTypeResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    form_type_request: FormTypeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_type_service().create_one_form_type(request, form_type_request)


@router.delete(
    "/{form_type_id}/", response_model=FormTypeResponse, status_code=HTTPStatus.OK
)
def delete_one(
    form_type_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_type_service().delete_one_form_type(form_type_id, request)


@router.put(
    "/{form_type_id}/", response_model=FormTypeResponse, status_code=HTTPStatus.OK
)
def update_one(
    form_type_id: int,
    request: Request,
    form_type_request: FormTypeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_form_type_service().update_one_form_type(
        form_type_id, request, form_type_request
    )
