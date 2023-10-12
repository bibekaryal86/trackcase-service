from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import TaskCalendar as TaskCalendarModel
from src.trackcase_service.utils.commons import (
    copy_objects,
    get_err_msg,
    raise_http_exception,
)

from .schemas import TaskCalendar as TaskCalendarSchema
from .schemas import TaskCalendarRequest, TaskCalendarResponse


class TaskCalendarService(CrudService):
    def __init__(self, db_session: Session):
        super(TaskCalendarService, self).__init__(db_session, TaskCalendarModel)

    def create_one_task_calendar(
        self, request: Request, request_object: TaskCalendarRequest
    ) -> TaskCalendarResponse:
        try:
            data_model: TaskCalendarModel = copy_objects(
                request_object, TaskCalendarModel
            )
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
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
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> TaskCalendarResponse:
        try:
            data_model: TaskCalendarModel = super().read_one(model_id)
            if data_model:
                schema_model: TaskCalendarSchema = _convert_model_to_schema(
                    data_model, is_include_extras
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )

    def read_all_task_calendars(
        self, request: Request, is_include_extras: bool
    ) -> TaskCalendarResponse:
        try:
            data_models: List[TaskCalendarModel] = super().read_all()
            schema_models: List[TaskCalendarSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
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
        task_calendar_response = self.read_one_task_calendar(model_id, request, False)

        if not (task_calendar_response and task_calendar_response.task_calendars):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: TaskCalendarModel = copy_objects(
                request_object, TaskCalendarModel
            )
            data_model = super().update(model_id, data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )

    def delete_one_task_calendar(
        self, model_id: int, request: Request
    ) -> TaskCalendarResponse:
        task_calendar_response = self.read_one_task_calendar(model_id, request, False)

        if not (task_calendar_response and task_calendar_response.task_calendars):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return TaskCalendarResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )


def get_task_calendar_service(db_session: Session) -> TaskCalendarService:
    return TaskCalendarService(db_session)


def get_response_single(single: TaskCalendarSchema) -> TaskCalendarResponse:
    return TaskCalendarResponse(task_calendars=[single])


def get_response_multiple(multiple: list[TaskCalendarSchema]) -> TaskCalendarResponse:
    return TaskCalendarResponse(task_calendars=multiple)


def _convert_model_to_schema(
    data_model: TaskCalendarModel, is_include_extras: bool = False
) -> TaskCalendarSchema:
    data_schema = TaskCalendarSchema(
        id=data_model.id,
        created=data_model.created,
        modified=data_model.modified,
        task_date=data_model.hearing_date,
        task_type_id=data_model.hearing_type_id,
        court_case_id=data_model.court_case_id,
        hearing_calendar_id=data_model.hearing_calendar_id,
    )
    if is_include_extras:
        data_schema.task_type = data_model.task_type
        data_schema.court_case = data_model.court_case
        data_schema.hearing_calendar = data_model.hearing_calendar
        data_schema.forms = data_model.forms
    return data_schema
