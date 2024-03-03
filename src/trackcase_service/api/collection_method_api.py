from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.collection_method_service import (
    get_collection_method_service,
)
from src.trackcase_service.service.schemas import (
    CollectionMethodRequest,
    CollectionMethodResponse,
)
from src.trackcase_service.utils.commons import raise_http_exception

router = APIRouter(
    prefix="/trackcase-service/collection_methods", tags=["CollectionMethods"]
)


@router.get("/", response_model=CollectionMethodResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_method_service(db_session).read_all_collection_methods(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{collection_method_id}/",
    response_model=CollectionMethodResponse,
    status_code=HTTPStatus.OK,
)
def find_one(
    collection_method_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    collection_method_response: (
        CollectionMethodResponse
    ) = get_collection_method_service(db_session).read_one_collection_method(
        collection_method_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if collection_method_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"CollectionMethod Not Found By Id: {collection_method_id}!!!",
        )
    return collection_method_response


@router.post("/", response_model=CollectionMethodResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    collection_method_request: CollectionMethodRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_method_service(db_session).create_one_collection_method(
        request, collection_method_request
    )


@router.delete(
    "/{collection_method_id}/",
    response_model=CollectionMethodResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    collection_method_id: int,
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_method_service(db_session).delete_one_collection_method(
        collection_method_id, request
    )


@router.put(
    "/{collection_method_id}/",
    response_model=CollectionMethodResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    collection_method_id: int,
    request: Request,
    collection_method_request: CollectionMethodRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_method_service(db_session).update_one_collection_method(
        collection_method_id, request, collection_method_request
    )
