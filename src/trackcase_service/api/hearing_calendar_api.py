from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.hearing_calendar_service import (
    get_hearing_calendar_service,
)
from src.trackcase_service.service.schemas import (
    HearingCalendarRequest,
    HearingCalendarResponse,
)
from src.trackcase_service.utils.commons import raise_http_exception

router = APIRouter(
    prefix="/trackcase-service/hearing_calendars", tags=["HearingCalendars"]
)


@router.get("/", response_model=HearingCalendarResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_hearing_calendar_service(db_session).read_all_hearing_calendars(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{hearing_calendar_id}/",
    response_model=HearingCalendarResponse,
    status_code=HTTPStatus.OK,
)
def find_one(
    hearing_calendar_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    hearing_calendar_response: HearingCalendarResponse = get_hearing_calendar_service(
        db_session
    ).read_one_hearing_calendar(
        hearing_calendar_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if hearing_calendar_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"HearingCalendar Not Found By Id: {hearing_calendar_id}!!!",
        )
    return hearing_calendar_response


@router.post("/", response_model=HearingCalendarResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    hearing_calendar_request: HearingCalendarRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_hearing_calendar_service(db_session).create_one_hearing_calendar(
        request, hearing_calendar_request
    )


@router.delete(
    "/{hearing_calendar_id}/",
    response_model=HearingCalendarResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    hearing_calendar_id: int,
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    return get_hearing_calendar_service(db_session).delete_one_hearing_calendar(
        hearing_calendar_id, request
    )


@router.put(
    "/{hearing_calendar_id}/",
    response_model=HearingCalendarResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    hearing_calendar_id: int,
    request: Request,
    hearing_calendar_request: HearingCalendarRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_hearing_calendar_service(db_session).update_one_hearing_calendar(
        hearing_calendar_id, request, hearing_calendar_request
    )
