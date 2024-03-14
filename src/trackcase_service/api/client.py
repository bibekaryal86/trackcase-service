from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.client import get_client_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post(
    "/",
    response_model=schemas.ClientResponse,
    status_code=HTTPStatus.OK,
)
def insert_client(
    request: Request,
    client_request: schemas.ClientRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).create_client(request, client_request)


@router.get(
    "/",
    response_model=schemas.ClientResponse,
    status_code=HTTPStatus.OK,
)
def find_client(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).read_client(request, request_metadata)


@router.put(
    "/{client_id}/",
    response_model=schemas.ClientResponse,
    status_code=HTTPStatus.OK,
)
def modify_client(
    client_id: int,
    request: Request,
    client_request: schemas.ClientRequest,
    is_restore: bool = Query(default=False),
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).update_client(
        client_id, request, client_request, is_restore
    )


@router.delete(
    "/{client_id}/{is_hard_delete}/",
    response_model=schemas.ClientResponse,
    status_code=HTTPStatus.OK,
)
def remove_client(
    client_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_client_service(db_session).delete_client(
        client_id, is_hard_delete, request
    )
