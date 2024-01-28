from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.court_service import get_court_service
from src.trackcase_service.service.schemas import CourtRequest, CourtResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
)

router = APIRouter(prefix="/trackcase-service/courts", tags=["Courts"])


@router.get("/", response_model=CourtResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).read_all_courts(
        request, is_include_extra, is_include_history
    )


@router.get("/{court_id}/", response_model=CourtResponse, status_code=HTTPStatus.OK)
def find_one(
    court_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    court_response: CourtResponse = get_court_service(db_session).read_one_court(
        court_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if court_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"Court Not Found By Id: {court_id}!!!",
        )
    return court_response


@router.post("/", response_model=CourtResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    court_request: CourtRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).create_one_court(request, court_request)


@router.delete("/{court_id}/", response_model=CourtResponse, status_code=HTTPStatus.OK)
def delete_one(
    court_id: int,
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).delete_one_court(court_id, request)


@router.put("/{court_id}/", response_model=CourtResponse, status_code=HTTPStatus.OK)
def update_one(
    court_id: int,
    request: Request,
    court_request: CourtRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_court_service(db_session).update_one_court(
        court_id, request, court_request
    )
