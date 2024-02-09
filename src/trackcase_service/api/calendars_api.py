import datetime
from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, Request
from sqlalchemy import Row, text
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.hearing_calendar_service import (
    get_hearing_calendar_service,
)
from src.trackcase_service.service.schemas import (
    CalendarEvent,
    CalendarResponse,
    HearingCalendar,
    TaskCalendar,
)
from src.trackcase_service.service.task_calendar_service import (
    get_task_calendar_service,
)
from src.trackcase_service.utils.constants import CalendarObjectTypes

router = APIRouter(prefix="/trackcase-service/calendars", tags=["Calendars Common"])


@router.get("/", response_model=CalendarResponse, status_code=HTTPStatus.OK)
def find_all(
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
    calendar_events = _get_calendar_events(
        db_session, hearing_calendars, task_calendars
    )
    return CalendarResponse(
        hearing_calendars=hearing_calendars,
        task_calendars=task_calendars,
        calendar_events=calendar_events,
    )


def _get_calendar_events(
    db_session: Session,
    hearing_calendars: list[HearingCalendar],
    task_calendars: list[TaskCalendar],
) -> list[CalendarEvent]:
    hearing_calendar_ids = [
        hearing_calendar.id for hearing_calendar in hearing_calendars
    ]
    task_calendar_ids = [task_calendar.id for task_calendar in task_calendars]
    hearing_calendar_sql_data = _get_hearing_calendar_sql_data(
        db_session, hearing_calendar_ids
    )
    task_calendar_sql_data = _get_task_calendar_sql_data(db_session, task_calendar_ids)
    calendar_events1 = _get_hearing_calendar_events(
        hearing_calendars, hearing_calendar_sql_data
    )
    calendar_events2 = _get_task_calendar_events(task_calendars, task_calendar_sql_data)
    return calendar_events1 + calendar_events2


def _get_hearing_calendar_sql_data(
    db_session: Session, hearing_calendar_ids: list[int]
) -> list[Row[Any]]:
    hearing_calendar_ids_str = ",".join(map(str, hearing_calendar_ids))
    statement = text(
        """
            SELECT a.id, b.name as hearing_type, d.name as client_name
            FROM hearing_calendar a
            INNER JOIN hearing_type b ON a.hearing_type_id = b.id
            INNER JOIN court_case c ON a.court_case_id = c.id
            INNER JOIN client d ON c.client_id = d.id
            WHERE a.id IN ({})
        """.format(
            hearing_calendar_ids_str
        )
    )
    return db_session.execute(statement)


def _get_task_calendar_sql_data(
    db_session: Session, task_calendar_ids: list[int]
) -> list[Row[Any]]:
    task_calendar_ids_str = ",".join(map(str, task_calendar_ids))
    statement1 = text(
        """
            SELECT a.id, b.name as task_type, e.name as client_name
            FROM task_calendar a
            INNER JOIN task_type b ON a.task_type_id = b.id
            INNER JOIN hearing_calendar c ON a.hearing_calendar_id = c.id
            INNER JOIN court_case d ON c.court_case_id = d.id
            INNER JOIN client e ON d.client_id = e.id
            WHERE a.id IN ({})
        """.format(
            task_calendar_ids_str
        )
    )

    results1 = db_session.execute(statement1)

    # Execute second part of the SQL query (form based)
    statement2 = text(
        """
            SELECT a.id, b.name as task_type, e.name as client_name
            FROM task_calendar a
            INNER JOIN task_type b ON a.task_type_id = b.id
            INNER JOIN form c ON a.form_id = c.id
            INNER JOIN court_case d ON c.court_case_id = d.id
            INNER JOIN client e ON d.client_id = e.id
            WHERE a.id IN ({})
        """.format(
            task_calendar_ids_str
        )
    )

    results2 = db_session.execute(statement2)

    return list(results1) + list(results2)


def _get_hearing_calendar_events(
    hearing_calendars: list[HearingCalendar], sql_results: list[Row[Any]]
) -> list[CalendarEvent]:
    calendar_events: list[CalendarEvent] = []

    def _match_hearing_calendar_data(hearing_calendar_id: int):
        matching_data = next(
            (row for row in sql_results if row.id == hearing_calendar_id), None
        )
        if matching_data:
            return f"{matching_data.client_name}, {matching_data.hearing_type}"
        return "NO_MATCHING_DATA"

    for hearing_calendar in hearing_calendars:
        event = CalendarEvent(
            id=hearing_calendar.id,
            type=CalendarObjectTypes.HEARING,
            date=hearing_calendar.hearing_date,
            isPastDue=(
                hearing_calendar.hearing_date.date() < datetime.date.today()
                and hearing_calendar.status not in ["COMPLETED", "CLOSED"]
            ),
            status=hearing_calendar.status,
            title=_match_hearing_calendar_data(hearing_calendar.id),
        )
        calendar_events.append(event)

    return calendar_events


def _get_task_calendar_events(
    task_calendars: list[TaskCalendar], sql_results: list[Row[Any]]
) -> list[CalendarEvent]:
    calendar_events: list[CalendarEvent] = []

    def _match_task_calendar_data(task_calendar_id: int):
        matching_data = next(
            (row for row in sql_results if row.id == task_calendar_id), None
        )
        if matching_data:
            return f"{matching_data.client_name}, {matching_data.task_type}"
        return "NO_MATCHING_DATA"

    for task_calendar in task_calendars:
        event = CalendarEvent(
            id=task_calendar.id,
            type=CalendarObjectTypes.TASK,
            date=task_calendar.task_date,
            isPastDue=(
                task_calendar.task_date.date() < datetime.date.today()
                and task_calendar.status not in ["COMPLETED", "CLOSED"]
            ),
            status=task_calendar.status,
            title=_match_task_calendar_data(task_calendar.id),
        )
        calendar_events.append(event)

    return calendar_events
