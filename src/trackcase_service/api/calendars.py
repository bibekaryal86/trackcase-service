import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.calendars import get_calendar_service
from src.trackcase_service.service.ref_types import get_ref_types_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/calendars", tags=["Calendars"])


@router.get("/all/", response_model=schemas.CalendarResponse, status_code=HTTPStatus.OK)
def get_calendars(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    hearing_calendars = (
        get_calendar_service(
            schemas.CalendarServiceRegistry.HEARING_CALENDAR, db_session
        )
        .read_hearing_calendar(request, request_metadata)
        .data
    )
    task_calendars = (
        get_calendar_service(schemas.CalendarServiceRegistry.TASK_CALENDAR, db_session)
        .read_task_calendar(request, request_metadata)
        .data
    )
    calendar_events = _get_calendar_events(
        hearing_calendars, task_calendars, request, db_session
    )
    calendar_response_data = schemas.CalendarResponseData(
        hearing_calendars=hearing_calendars,
        task_calendars=task_calendars,
        calendar_events=calendar_events,
    )
    return schemas.CalendarResponse(data=calendar_response_data)


# hearing calendar
@router.post(
    "/hearing/",
    response_model=schemas.HearingCalendarResponse,
    status_code=HTTPStatus.OK,
)
def insert_hearing_calendar(
    request: Request,
    hearing_calendar_request: schemas.HearingCalendarRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.HEARING_CALENDAR, db_session
    ).create_hearing_calendar(request, hearing_calendar_request)


@router.get(
    "/hearing/",
    response_model=schemas.HearingCalendarResponse,
    status_code=HTTPStatus.OK,
)
def find_hearing_calendar(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.HEARING_CALENDAR, db_session
    ).read_hearing_calendar(request, request_metadata)


@router.put(
    "/hearing/{hearing_calendar_id}/",
    response_model=schemas.HearingCalendarResponse,
    status_code=HTTPStatus.OK,
)
def modify_hearing_calendar(
    hearing_calendar_id: int,
    request: Request,
    hearing_calendar_request: schemas.HearingCalendarRequest,
    is_restore: bool = Query(default=False),
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.HEARING_CALENDAR, db_session
    ).update_hearing_calendar(
        hearing_calendar_id, request, hearing_calendar_request, is_restore
    )


@router.delete(
    "/hearing/{hearing_calendar_id}/{is_hard_delete}/",
    response_model=schemas.HearingCalendarResponse,
    status_code=HTTPStatus.OK,
)
def remove_hearing_calendar(
    hearing_calendar_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.HEARING_CALENDAR, db_session
    ).delete_hearing_calendar(hearing_calendar_id, is_hard_delete, request)


# task calendar
@router.post(
    "/task/",
    response_model=schemas.TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def insert_task_calendar(
    request: Request,
    task_calendar_request: schemas.TaskCalendarRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.TASK_CALENDAR, db_session
    ).create_task_calendar(request, task_calendar_request)


@router.get(
    "/task/",
    response_model=schemas.TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def find_task_calendar(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.TASK_CALENDAR, db_session
    ).read_task_calendar(request, request_metadata)


@router.put(
    "/task/{task_calendar_id}/",
    response_model=schemas.TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def modify_task_calendar(
    task_calendar_id: int,
    request: Request,
    task_calendar_request: schemas.TaskCalendarRequest,
    is_restore: bool = Query(default=False),
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.TASK_CALENDAR, db_session
    ).update_task_calendar(task_calendar_id, request, task_calendar_request, is_restore)


@router.delete(
    "/task/{task_calendar_id}/{is_hard_delete}/",
    response_model=schemas.TaskCalendarResponse,
    status_code=HTTPStatus.OK,
)
def remove_task_calendar(
    task_calendar_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_calendar_service(
        schemas.CalendarServiceRegistry.TASK_CALENDAR, db_session
    ).delete_task_calendar(task_calendar_id, is_hard_delete, request)


def _get_calendar_events(
    hearing_calendars: list[schemas.HearingCalendar],
    task_calendars: list[schemas.TaskCalendar],
    request: Request,
    db_session: Session,
) -> list[schemas.CalendarEvent]:
    calendar_events = []
    for hearing_calendar in hearing_calendars:
        calendar_event = schemas.CalendarEvent(
            id=hearing_calendar.id,
            calendar=schemas.CalendarObjectTypes.HEARING,
            type=hearing_calendar.hearing_type.name,
            date=hearing_calendar.hearing_date,
            status=_check_and_set_status(
                hearing_calendar.component_status_id,
                hearing_calendar.hearing_date,
                request,
                db_session,
            ),
            title=hearing_calendar.court_case.client.name,
            court_case_id=hearing_calendar.court_case_id,
        )
        calendar_events.append(calendar_event)

    for task_calendar in task_calendars:
        calendar_event = schemas.CalendarEvent(
            id=task_calendar.id,
            calendar=schemas.CalendarObjectTypes.TASK,
            type=task_calendar.task_type.name,
            date=task_calendar.task_date,
            status=_check_and_set_status(
                task_calendar.component_status_id, task_calendar.task_date, request, db_session
            ),
            title=(
                task_calendar.filing.court_case.client.name
                if task_calendar.filing_id
                else task_calendar.hearing_calendar.court_case.client.name
            ),
            court_case_id=(
                task_calendar.filing.court_case_id
                if task_calendar.filing_id
                else task_calendar.hearing_calendar.court_case_id
            ),
        )
        calendar_events.append(calendar_event)
    return calendar_events


def _check_and_set_status(
    component_status_id: int,
    date: datetime.datetime,
    request: Request,
    db_session: Session,
) -> str:
    calendar_inactive_statuses = get_ref_types_service(
        service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
        db_session=db_session,
    ).get_component_status(
        request,
        schemas.ComponentStatusNames.CALENDARS,
        schemas.ComponentStatusTypes.INACTIVE,
    )
    calendar_inactive_statuses = [
        component_status.id for component_status in calendar_inactive_statuses
    ]

    if date.date() < datetime.date.today():
        if component_status_id in calendar_inactive_statuses:
            return "PAST_DONE"
        else:
            return "PAST_DUE"
    elif component_status_id in calendar_inactive_statuses:
        return "DONE"
    else:
        return "DUE"
