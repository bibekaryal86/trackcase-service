from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import (
    HistoryTaskCalendar as HistoryTaskCalendarModel,
)
from src.trackcase_service.db.models import TaskCalendar as TaskCalendarModel
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import TaskCalendar as TaskCalendarSchema
from src.trackcase_service.service.schemas import (
    TaskCalendarRequest,
    TaskCalendarResponse,
)
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_request_schema_to_model,
    convert_task_calendar_model_to_schema,
)


class TaskCalendarService(CrudService):
    def __init__(self, db_session: Session):
        super(TaskCalendarService, self).__init__(db_session, TaskCalendarModel)

    def create_one_task_calendar(
        self, request: Request, request_object: TaskCalendarRequest
    ) -> TaskCalendarResponse:
        try:
            data_model: TaskCalendarModel = convert_request_schema_to_model(
                request_object, TaskCalendarModel
            )
            data_model = super().create(data_model)
            _handle_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_task_calendar_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting TaskCalendar. Please Try Again!!!", str(ex)
                ),
            )

    def read_one_task_calendar(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> TaskCalendarResponse:
        try:
            data_model: TaskCalendarModel = super().read_one(model_id)
            if data_model:
                schema_model: TaskCalendarSchema = (
                    convert_task_calendar_model_to_schema(
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
                    f"Error Retrieving TaskCalendar By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_task_calendars(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> TaskCalendarResponse:
        try:
            data_models: List[TaskCalendarModel] = super().read_all(
                sort_direction="desc", sort_by="task_date"
            )
            schema_models: List[TaskCalendarSchema] = [
                convert_task_calendar_model_to_schema(
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
                    "Error Retrieving TaskCalendars. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_task_calendar(
        self, model_id: int, request: Request, request_object: TaskCalendarRequest
    ) -> TaskCalendarResponse:
        task_calendar_response = self.read_one_task_calendar(model_id, request)

        if not (task_calendar_response and task_calendar_response.task_calendars):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"TaskCalendar Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: TaskCalendarModel = convert_request_schema_to_model(
                request_object, TaskCalendarModel
            )
            data_model = super().update(model_id, data_model)
            _handle_history(self.db_session, request, model_id, request_object)
            schema_model = convert_task_calendar_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating TaskCalendar By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_task_calendar(
        self, model_id: int, request: Request
    ) -> TaskCalendarResponse:
        task_calendar_response = self.read_one_task_calendar(model_id, request)

        if not (task_calendar_response and task_calendar_response.task_calendars):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"TaskCalendar Not Found By Id: {model_id}!!!",
            )

        try:
            _handle_history(self.db_session, request, model_id, is_delete=True)
            super().delete(model_id)
            return TaskCalendarResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting TaskCalendar By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_task_calendar_service(db_session: Session) -> TaskCalendarService:
    return TaskCalendarService(db_session)


def get_response_single(single: TaskCalendarSchema) -> TaskCalendarResponse:
    return TaskCalendarResponse(task_calendars=[single])


def get_response_multiple(multiple: list[TaskCalendarSchema]) -> TaskCalendarResponse:
    return TaskCalendarResponse(task_calendars=multiple)


def _handle_history(
    db_session: Session,
    request: Request,
    task_calendar_id: int,
    request_object: TaskCalendarRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryTaskCalendarModel)
    if is_delete:
        history_service.delete_history_before_delete_object(
            HistoryTaskCalendarModel.__tablename__,
            "task_calendar_id",
            task_calendar_id,
            "TaskCalendar",
            "HistoryTaskCalendar",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "task_calendar_id",
            task_calendar_id,
            "TaskCalendar",
            "HistoryTaskCalendar",
        )
