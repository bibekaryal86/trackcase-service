from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import HearingCalendar as HearingCalendarModel
from src.trackcase_service.db.models import (
    HistoryHearingCalendar as HistoryHearingCalendarModel,
)
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import (
    HearingCalendar as HearingCalendarSchema,
)
from src.trackcase_service.service.schemas import (
    HearingCalendarRequest,
    HearingCalendarResponse,
    TaskCalendarRequest,
)
from src.trackcase_service.service.task_calendar_service import (
    get_task_calendar_service,
)
from src.trackcase_service.utils.commons import (
    check_active_task_calendars,
    get_err_msg,
    raise_http_exception,
)
from src.trackcase_service.utils.constants import (
    DEFAULT_HEARING_TO_TASK_CALENDAR_DATE,
    HEARING_TO_TASK_CALENDAR_DATE,
    TASK_ID_DUE_AT_HEARING,
    get_statuses,
)
from src.trackcase_service.utils.convert import (
    convert_hearing_calendar_model_to_schema,
    convert_request_schema_to_model,
)


class HearingCalendarService(CrudService):
    def __init__(self, db_session: Session):
        super(HearingCalendarService, self).__init__(db_session, HearingCalendarModel)

    def create_one_hearing_calendar(
        self, request: Request, request_object: HearingCalendarRequest
    ) -> HearingCalendarResponse:
        try:
            data_model: HearingCalendarModel = convert_request_schema_to_model(
                request_object, HearingCalendarModel
            )
            data_model = super().create(data_model)
            _handle_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_hearing_calendar_model_to_schema(data_model)
            _create_task_calendar(self.db_session, request, schema_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting HearingCalendar. Please Try Again!!!", str(ex)
                ),
            )

    def read_one_hearing_calendar(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> HearingCalendarResponse:
        try:
            data_model: HearingCalendarModel = super().read_one(model_id)
            if data_model:
                schema_model: HearingCalendarSchema = (
                    convert_hearing_calendar_model_to_schema(
                        data_model,
                        is_include_extra,
                        is_include_history,
                    )
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving HearingCalendar By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )

    def read_all_hearing_calendars(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> HearingCalendarResponse:
        try:
            sort_config = {"hearing_date": "desc"}
            data_models: List[HearingCalendarModel] = super().read_all(sort_config)
            schema_models: List[HearingCalendarSchema] = [
                convert_hearing_calendar_model_to_schema(
                    data_model,
                    is_include_extra,
                    is_include_history,
                )
                for data_model in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving HearingCalendars. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_hearing_calendar(
        self, model_id: int, request: Request, request_object: HearingCalendarRequest
    ) -> HearingCalendarResponse:
        hearing_calendar_response = self.read_one_hearing_calendar(
            model_id, request, is_include_extra=True
        )

        if not (
            hearing_calendar_response and hearing_calendar_response.hearing_calendars
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"HearingCalendar Not Found By Id: {model_id}!!!",
            )

        _check_dependents_statuses(
            request,
            request_object.status,
            hearing_calendar_response.hearing_calendars[0],
        )

        try:
            data_model: HearingCalendarModel = convert_request_schema_to_model(
                request_object, HearingCalendarModel
            )
            data_model = super().update(model_id, data_model)
            _handle_history(self.db_session, request, model_id, request_object)
            schema_model = convert_hearing_calendar_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating HearingCalendar By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )

    def delete_one_hearing_calendar(
        self, model_id: int, request: Request
    ) -> HearingCalendarResponse:
        hearing_calendar_response = self.read_one_hearing_calendar(
            model_id, request, is_include_extra=True
        )

        if not (
            hearing_calendar_response and hearing_calendar_response.hearing_calendars
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"HearingCalendar Not Found By Id: {model_id}!!!",
            )

        _check_dependents(request, hearing_calendar_response.hearing_calendars[0])
        _handle_history(self.db_session, request, model_id, is_delete=True)

        try:
            super().delete(model_id)
            return HearingCalendarResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting HearingCalendar By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )


def get_hearing_calendar_service(db_session: Session) -> HearingCalendarService:
    return HearingCalendarService(db_session)


def get_response_single(single: HearingCalendarSchema) -> HearingCalendarResponse:
    return HearingCalendarResponse(hearing_calendars=[single])


def get_response_multiple(
    multiple: list[HearingCalendarSchema],
) -> HearingCalendarResponse:
    return HearingCalendarResponse(hearing_calendars=multiple)


def _check_dependents_statuses(
    request: Request,
    status_new: str,
    hearing_calendar_old: HearingCalendarSchema,
):
    status_old = hearing_calendar_old.status
    inactive_statuses = get_statuses().get("hearing_calendar").get("inactive")
    if status_new != status_old and status_new in inactive_statuses:
        if check_active_task_calendars(hearing_calendar_old.task_calendars):
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Update Hearing Calendar {hearing_calendar_old.id} Status to {status_new}, There are Active Task Calendars!",  # noqa: E501
            )


def _check_dependents(request: Request, hearing_calendar: HearingCalendarSchema):
    if hearing_calendar.task_calendars:
        raise_http_exception(
            request,
            HTTPStatus.UNPROCESSABLE_ENTITY,
            f"Cannot Delete Hearing Calendar {hearing_calendar.id}, There are Linked Task Calendars!",  # noqa: E501
        )


def _handle_history(
    db_session: Session,
    request: Request,
    hearing_calendar_id: int,
    request_object: HearingCalendarRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryHearingCalendarModel)
    if is_delete:
        history_service.delete_history_before_delete_object(
            HistoryHearingCalendarModel.__tablename__,
            "hearing_calendar_id",
            hearing_calendar_id,
            "HearingCalendar",
            "HistoryHearingCalendar",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "hearing_calendar_id",
            hearing_calendar_id,
            "HearingCalendar",
            "HistoryHearingCalendar",
        )


def _create_task_calendar(
    db_session: Session, request: Request, hearing_calendar: HearingCalendarSchema
):
    task_date_diff: int = (
        HEARING_TO_TASK_CALENDAR_DATE.get(hearing_calendar.hearing_type.name)
        or DEFAULT_HEARING_TO_TASK_CALENDAR_DATE
    )
    task_date: datetime = hearing_calendar.hearing_date - timedelta(days=task_date_diff)
    due_date: datetime = hearing_calendar.hearing_date - timedelta(days=3)
    current_date = datetime.now()
    if task_date < current_date:
        task_date = current_date

    task_calendar_request = TaskCalendarRequest(
        task_date=task_date,
        due_date=due_date,
        task_type_id=TASK_ID_DUE_AT_HEARING,
        hearing_calendar_id=hearing_calendar.id,
        status=hearing_calendar.status,
    )
    get_task_calendar_service(db_session).create_one_task_calendar(
        request=request, request_object=task_calendar_request
    )
