from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

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

router = APIRouter(prefix="/trackcase-service/task_calendars", tags=["TaskCalendars"])


@router.get("/", response_model=TaskCalendarResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service().read_all_task_calendars(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{task_calendar_id}/",
    response_model=TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def find_one(
    task_calendar_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    task_calendar_response: TaskCalendarResponse = (
        get_task_calendar_service().read_one_task_calendar(
            task_calendar_id,
            request,
            is_include_extra,
            is_include_history,
        )
    )
    if task_calendar_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"TaskCalendar Not Found By Id: {task_calendar_id}!!!",
        )
    return task_calendar_response


@router.post("/", response_model=TaskCalendarResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    task_calendar_request: TaskCalendarRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service().create_one_task_calendar(
        request, task_calendar_request
    )


@router.delete(
    "/{task_calendar_id}/",
    response_model=TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    task_calendar_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service().delete_one_task_calendar(
        task_calendar_id, request
    )


@router.put(
    "/{task_calendar_id}/",
    response_model=TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    task_calendar_id: int,
    request: Request,
    task_calendar_request: TaskCalendarRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_calendar_service().update_one_task_calendar(
        task_calendar_id, request, task_calendar_request
    )
