from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.cash_collection_service import (
    get_cash_collection_service,
)
from src.trackcase_service.service.schemas import (
    CashCollectionRequest,
    CashCollectionResponse,
)
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/cash_collections", tags=["CashCollections"])


@router.get("/", response_model=CashCollectionResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service(db_session).read_all_cash_collections(
        request, is_include_extras
    )


@router.get(
    "/{cash_collection_id}",
    response_model=CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def find_one(
    cash_collection_id: int,
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    cash_collection_response: CashCollectionResponse = get_cash_collection_service(
        db_session
    ).read_one_cash_collection(cash_collection_id, request, is_include_extras)
    if cash_collection_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"CashCollection Not Found By Id: {cash_collection_id}!!!",
            f"CashCollection Not Found By Id: {cash_collection_id}!!!",
        )
    return cash_collection_response


@router.post("/", response_model=CashCollectionResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    cash_collection_request: CashCollectionRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service(db_session).create_one_cash_collection(
        request, cash_collection_request
    )


@router.delete(
    "/{cash_collection_id}",
    response_model=CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    cash_collection_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service(db_session).delete_one_cash_collection(
        cash_collection_id, request
    )


@router.put(
    "/{cash_collection_id}",
    response_model=CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    cash_collection_id: int,
    request: Request,
    cash_collection_request: CashCollectionRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service(db_session).update_one_cash_collection(
        cash_collection_id, request, cash_collection_request
    )