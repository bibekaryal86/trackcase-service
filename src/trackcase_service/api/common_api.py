import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.case_type_service import get_case_type_service
from src.trackcase_service.service.collection_method_service import (
    get_collection_method_service,
)
from src.trackcase_service.service.form_type_service import get_form_type_service
from src.trackcase_service.service.hearing_calendar_service import (
    get_hearing_calendar_service,
)
from src.trackcase_service.service.hearing_type_service import get_hearing_type_service
from src.trackcase_service.service.schemas import (
    CalendarEvent,
    CalendarObjectTypes,
    CalendarResponse,
    HearingCalendar,
    TaskCalendar,
)
from src.trackcase_service.service.task_calendar_service import (
    get_task_calendar_service,
)
from src.trackcase_service.service.task_type_service import get_task_type_service
from src.trackcase_service.utils import constants

router = APIRouter(prefix="/trackcase-service/common", tags=["Common"])


@router.get("/statuses/", summary="Get Statuses")
def get_statuses():
    return constants.get_statuses()


@router.get("/calendars/", response_model=CalendarResponse, status_code=HTTPStatus.OK)
def get_calendars(
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    hearing_calendars = (
        get_hearing_calendar_service(db_session)
        .read_all_hearing_calendars(request)
        .hearing_calendars
    )
    task_calendars = (
        get_task_calendar_service(db_session)
        .read_all_task_calendars(request)
        .task_calendars
    )
    calendar_events = _get_calendar_events(hearing_calendars, task_calendars)
    return CalendarResponse(
        hearing_calendars=hearing_calendars,
        task_calendars=task_calendars,
        calendar_events=calendar_events,
    )


@router.get("/ref_types/", tags=["Common"], summary="Get All Ref Types")
def get_all_ref_types(
    request: Request,
    components: str = Query(default=""),
    db_session: Session = Depends(get_db_session),
):
    all_ref_types = {}
    if not components:
        components = (
            "statuses,case_types,collection_methods,form_types,hearing_types,task_types"
        )
    component_list = components.split(",")
    for component in component_list:
        if component == "statuses":
            all_ref_types["statuses"] = constants.get_statuses()
        if component == "case_types":
            all_ref_types["case_types"] = get_case_type_service(
                db_session
            ).read_all_case_types(request)
        if component == "collection_methods":
            all_ref_types["collection_methods"] = get_collection_method_service(
                db_session
            ).read_all_collection_methods(request)
        if component == "form_types":
            all_ref_types["form_types"] = get_form_type_service(
                db_session
            ).read_all_form_types(request)
        if component == "hearing_types":
            all_ref_types["hearing_types"] = get_hearing_type_service(
                db_session
            ).read_all_hearing_types(request)
        if component == "task_types":
            all_ref_types["task_types"] = get_task_type_service(
                db_session
            ).read_all_task_types(request)
    return all_ref_types


def _get_calendar_events(
    hearing_calendars: list[HearingCalendar],
    task_calendars: list[TaskCalendar],
) -> list[CalendarEvent]:
    calendar_events = []
    for hearing_calendar in hearing_calendars:
        calendar_event = CalendarEvent(
            id=hearing_calendar.id,
            calendar=CalendarObjectTypes.HEARING,
            type=hearing_calendar.hearing_type.name,
            date=hearing_calendar.hearing_date,
            status=check_and_set_status(
                hearing_calendar.status, hearing_calendar.hearing_date
            ),
            title=hearing_calendar.court_case.client.name,
            court_case_id=hearing_calendar.court_case_id,
        )
        calendar_events.append(calendar_event)

    for task_calendar in task_calendars:
        calendar_event = CalendarEvent(
            id=task_calendar.id,
            calendar=CalendarObjectTypes.TASK,
            type=task_calendar.task_type.name,
            date=task_calendar.task_date,
            status=check_and_set_status(task_calendar.status, task_calendar.task_date),
            title=(
                task_calendar.form.court_case.client.name
                if task_calendar.form_id
                else task_calendar.hearing_calendar.court_case.client.name
            ),
            court_case_id=(
                task_calendar.form.court_case_id
                if task_calendar.form_id
                else task_calendar.hearing_calendar.court_case_id
            ),
        )
        calendar_events.append(calendar_event)
    return calendar_events


def check_and_set_status(status: str, date: datetime) -> str:
    completed_statuses = get_statuses().get("calendars").get("inactive")
    if date.date() < datetime.date.today():
        if status in completed_statuses:
            return "PAST_DONE"
        else:
            return "PAST_DUE"
    elif status in completed_statuses:
        return "DONE"
    else:
        return "DUE"
