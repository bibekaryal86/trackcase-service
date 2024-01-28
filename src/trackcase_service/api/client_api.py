from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.service.client_service import get_client_service
from src.trackcase_service.service.schemas import ClientRequest, ClientResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/clients", tags=["Clients"])


@router.get("/", response_model=ClientResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service().read_all_clients(
        request, is_include_extra, is_include_history
    )


@router.get("/{client_id}/", response_model=ClientResponse, status_code=HTTPStatus.OK)
def find_one(
    client_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    client_response: ClientResponse = get_client_service().read_one_client(
        client_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if client_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"Client Not Found By Id: {client_id}!!!",
        )
    return client_response


@router.post("/", response_model=ClientResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    client_request: ClientRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service().create_one_client(request, client_request)


@router.delete(
    "/{client_id}/", response_model=ClientResponse, status_code=HTTPStatus.OK
)
def delete_one(
    client_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service().delete_one_client(client_id, request)


@router.put("/{client_id}/", response_model=ClientResponse, status_code=HTTPStatus.OK)
def update_one(
    client_id: int,
    request: Request,
    client_request: ClientRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service().update_one_client(client_id, request, client_request)
