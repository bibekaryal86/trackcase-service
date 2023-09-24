from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.schemas import (
    TaskCalendarRequest,
    TaskCalendarResponse,
)
from src.trackcase_service.service.task_calendar_service import (
    get_task_calendar_service,
)
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/task_calendars", tags=["TaskCalendars"])


@router.get("/", response_model=TaskCalendarResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service(db_session).read_all_task_calendars(
        request, is_include_extras
    )


@router.get(
    "/{task_calendar_id}",
    response_model=TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def find_one(
    task_calendar_id: int,
    request: Request,
    is_include_extras: bool = True,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    task_calendar_response: TaskCalendarResponse = get_task_calendar_service(
        db_session
    ).read_one_task_calendar(task_calendar_id, request, is_include_extras)
    if task_calendar_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"TaskCalendar Not Found By Id: {task_calendar_id}!!!",
            f"TaskCalendar Not Found By Id: {task_calendar_id}!!!",
        )
    return task_calendar_response


@router.post("/", response_model=TaskCalendarResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    task_calendar_request: TaskCalendarRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service(db_session).create_one_task_calendar(
        request, task_calendar_request
    )


@router.delete(
    "/{task_calendar_id}",
    response_model=TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    task_calendar_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service(db_session).delete_one_task_calendar(
        task_calendar_id, request
    )


@router.put(
    "/{task_calendar_id}",
    response_model=TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    task_calendar_id: int,
    request: Request,
    task_calendar_request: TaskCalendarRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service(db_session).update_one_task_calendar(
        task_calendar_id, request, task_calendar_request
    )
