from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.client_service import get_client_service
from src.trackcase_service.service.schemas import ClientRequest, ClientResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
)

router = APIRouter(prefix="/trackcase-service/clients", tags=["Clients"])


@router.get("/", response_model=ClientResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).read_all_clients(
        request, is_include_extra, is_include_history
    )


@router.get("/{client_id}/", response_model=ClientResponse, status_code=HTTPStatus.OK)
def find_one(
    client_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    client_response: ClientResponse = get_client_service(db_session).read_one_client(
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
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).create_one_client(request, client_request)


@router.delete(
    "/{client_id}/", response_model=ClientResponse, status_code=HTTPStatus.OK
)
def delete_one(
    client_id: int,
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).delete_one_client(client_id, request)


@router.put("/{client_id}/", response_model=ClientResponse, status_code=HTTPStatus.OK)
def update_one(
    client_id: int,
    request: Request,
    client_request: ClientRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).update_one_client(
        client_id, request, client_request
    )
