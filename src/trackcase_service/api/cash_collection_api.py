from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

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

router = APIRouter(
    prefix="/trackcase-service/cash_collections", tags=["CashCollections"]
)


@router.get("/", response_model=CashCollectionResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service().read_all_cash_collections(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{cash_collection_id}/",
    response_model=CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def find_one(
    cash_collection_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    cash_collection_response: CashCollectionResponse = (
        get_cash_collection_service().read_one_cash_collection(
            cash_collection_id,
            request,
            is_include_extra,
            is_include_history,
        )
    )
    if cash_collection_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"CashCollection Not Found By Id: {cash_collection_id}!!!",
        )
    return cash_collection_response


@router.post("/", response_model=CashCollectionResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    cash_collection_request: CashCollectionRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service().create_one_cash_collection(
        request, cash_collection_request
    )


@router.delete(
    "/{cash_collection_id}/",
    response_model=CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    cash_collection_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service().delete_one_cash_collection(
        cash_collection_id, request
    )


@router.put(
    "/{cash_collection_id}/",
    response_model=CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    cash_collection_id: int,
    request: Request,
    cash_collection_request: CashCollectionRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_cash_collection_service().update_one_cash_collection(
        cash_collection_id, request, cash_collection_request
    )
