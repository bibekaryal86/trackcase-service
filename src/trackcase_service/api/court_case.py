from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.court_case import get_court_case_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/court_cases", tags=["Court Cases"])


@router.post(
    "/",
    response_model=schemas.CourtCaseResponse,
    status_code=HTTPStatus.OK,
)
def insert_court_case(
    request: Request,
    court_case_request: schemas.CourtCaseRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).create_court_case(
        request, court_case_request
    )


@router.get(
    "/",
    response_model=schemas.CourtCaseResponse,
    status_code=HTTPStatus.OK,
)
def find_court_case(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).read_court_case(request, request_metadata)


@router.put(
    "/{court_case_id}/",
    response_model=schemas.CourtCaseResponse,
    status_code=HTTPStatus.OK,
)
def modify_court_case(
    court_case_id: int,
    request: Request,
    court_case_request: schemas.CourtCaseRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).update_court_case(
        court_case_id, request, court_case_request
    )


@router.delete(
    "/{court_case_id}/{is_hard_delete}/",
    response_model=schemas.CourtCaseResponse,
    status_code=HTTPStatus.OK,
)
def remove_court_case(
    court_case_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).delete_court_case(
        court_case_id, is_hard_delete, request
    )
