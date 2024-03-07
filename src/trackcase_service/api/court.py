from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.court import get_court_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/courts", tags=["Courts"])


@router.post(
    "/",
    response_model=schemas.CourtResponse,
    status_code=HTTPStatus.OK,
)
def insert_court(
    request: Request,
    court_request: schemas.CourtRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).create_court(request, court_request)


@router.get(
    "/",
    response_model=schemas.CourtResponse,
    status_code=HTTPStatus.OK,
)
def find_court(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).read_court(request, request_metadata)


@router.put(
    "/{court_id}/",
    response_model=schemas.CourtResponse,
    status_code=HTTPStatus.OK,
)
def modify_court(
    court_id: int,
    request: Request,
    court_request: schemas.CourtRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).update_court(court_id, request, court_request)


@router.delete(
    "/{court_id}/{is_hard_delete}/",
    response_model=schemas.CourtResponse,
    status_code=HTTPStatus.OK,
)
def remove_court(
    court_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).delete_court(court_id, is_hard_delete, request)
