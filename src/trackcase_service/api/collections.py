from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.collections import get_collection_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/collections", tags=["Collections"])


# case collection
@router.post(
    "/case/",
    response_model=schemas.CaseCollectionResponse,
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
def insert_case_collection(
    request: Request,
    case_collection_request: schemas.CaseCollectionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASE_COLLECTION, db_session
    ).create_case_collection(request, case_collection_request)


@router.get(
    "/case/",
    response_model=schemas.CaseCollectionResponse,
    status_code=HTTPStatus.OK,
)
def find_case_collection(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASE_COLLECTION, db_session
    ).read_case_collection(request, request_metadata)


@router.put(
    "/case/{case_collection_id}/",
    response_model=schemas.CaseCollectionResponse,
    status_code=HTTPStatus.OK,
)
def modify_case_collection(
    case_collection_id: int,
    request: Request,
    case_collection_request: schemas.CaseCollectionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASE_COLLECTION, db_session
    ).update_case_collection(case_collection_id, request, case_collection_request)


@router.delete(
    "/case/{case_collection_id}/{is_hard_delete}/",
    response_model=schemas.CaseCollectionResponse,
    status_code=HTTPStatus.OK,
)
def remove_case_collection(
    case_collection_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASE_COLLECTION, db_session
    ).delete_case_collection(case_collection_id, is_hard_delete, request)


# cash collection
@router.post(
    "/cash/",
    response_model=schemas.CashCollectionResponse,
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
def insert_cash_collection(
    request: Request,
    cash_collection_request: schemas.CashCollectionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASH_COLLECTION, db_session
    ).create_cash_collection(request, cash_collection_request)


@router.get(
    "/cash/",
    response_model=schemas.CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def find_cash_collection(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASH_COLLECTION, db_session
    ).read_cash_collection(request, request_metadata)


@router.put(
    "/cash/{cash_collection_id}/",
    response_model=schemas.CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def modify_cash_collection(
    cash_collection_id: int,
    request: Request,
    cash_collection_request: schemas.CashCollectionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASH_COLLECTION, db_session
    ).update_cash_collection(cash_collection_id, request, cash_collection_request)


@router.delete(
    "/cash/{cash_collection_id}/{is_hard_delete}/",
    response_model=schemas.CashCollectionResponse,
    status_code=HTTPStatus.OK,
)
def remove_cash_collection(
    cash_collection_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_collection_service(
        schemas.CollectionServiceRegistry.CASH_COLLECTION, db_session
    ).delete_cash_collection(cash_collection_id, is_hard_delete, request)
