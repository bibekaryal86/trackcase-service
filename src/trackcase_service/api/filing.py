from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.filing import (
    get_filing_rfe_service,
    get_filing_service,
)
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/filings", tags=["Filings"])


@router.post(
    "/filing/",
    response_model=schemas.FilingResponse,
    status_code=HTTPStatus.OK,
)
def insert_filing(
    request: Request,
    filing_request: schemas.FilingRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_filing_service(db_session).create_filing(request, filing_request)


@router.get(
    "/filing/",
    response_model=schemas.FilingResponse,
    status_code=HTTPStatus.OK,
)
def find_filing(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_filing_service(db_session).read_filing(request, request_metadata)


@router.put(
    "/filing/{filing_id}/",
    response_model=schemas.FilingResponse,
    status_code=HTTPStatus.OK,
)
def modify_filing(
    filing_id: int,
    request: Request,
    filing_request: schemas.FilingRequest,
    is_restore: bool = Query(default=False),
    db_session: Session = Depends(get_db_session),
):
    return get_filing_service(db_session).update_filing(
        filing_id, request, filing_request, is_restore
    )


@router.delete(
    "/filing/{filing_id}/{is_hard_delete}/",
    response_model=schemas.FilingResponse,
    status_code=HTTPStatus.OK,
)
def remove_filing(
    filing_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_filing_service(db_session).delete_filing(
        filing_id, is_hard_delete, request
    )


@router.post(
    "/rfe/",
    response_model=schemas.FilingRfeResponse,
    status_code=HTTPStatus.OK,
)
def insert_filing_rfe(
    request: Request,
    filing_rfe_request: schemas.FilingRfeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_filing_rfe_service(db_session).create_filing_rfe(
        request, filing_rfe_request
    )


@router.get(
    "/rfe/",
    response_model=schemas.FilingResponse,
    status_code=HTTPStatus.OK,
)
def find_filing_rfe(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_filing_rfe_service(db_session).read_filing_rfe(request, request_metadata)


@router.put(
    "/rfe/{filing_rfe_id}/",
    response_model=schemas.FilingRfeResponse,
    status_code=HTTPStatus.OK,
)
def modify_filing_rfe(
    filing_rfe_id: int,
    request: Request,
    filing_rfe_request: schemas.FilingRfeRequest,
    is_restore: bool = Query(default=False),
    db_session: Session = Depends(get_db_session),
):
    return get_filing_rfe_service(db_session).update_filing_rfe(
        filing_rfe_id, request, filing_rfe_request, is_restore
    )


@router.delete(
    "/rfe/{filing_rfe_id}/{is_hard_delete}/",
    response_model=schemas.FilingRfeResponse,
    status_code=HTTPStatus.OK,
)
def remove_filing_rfe(
    filing_rfe_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_filing_rfe_service(db_session).delete_filing_rfe(
        filing_rfe_id, is_hard_delete, request
    )
