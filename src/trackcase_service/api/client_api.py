from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
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
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service(db_session).read_all_clients(request, is_include_extras)


@router.get("/{client_id}", response_model=ClientResponse, status_code=HTTPStatus.OK)
def find_one(
    client_id: int,
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    client_response: ClientResponse = get_client_service(db_session).read_one_client(
        client_id, request, is_include_extras
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
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service(db_session).create_one_client(request, client_request)


@router.delete("/{client_id}", response_model=ClientResponse, status_code=HTTPStatus.OK)
def delete_one(
    client_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service(db_session).delete_one_client(client_id, request)


@router.put("/{client_id}", response_model=ClientResponse, status_code=HTTPStatus.OK)
def update_one(
    client_id: int,
    request: Request,
    client_request: ClientRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_client_service(db_session).update_one_client(
        client_id, request, client_request
    )
