from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import TaskType as TaskTypeModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import TaskType as TaskTypeSchema
from .schemas import TaskTypeRequest, TaskTypeResponse


class TaskTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(TaskTypeService, self).__init__(db_session, TaskTypeModel)

    def create_one_task_type(
        self, request: Request, request_object: TaskTypeRequest
    ) -> TaskTypeResponse:
        try:
            data_model: TaskTypeModel = copy_objects(request_object, TaskTypeModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting TaskType. Please Try Again!!!",
                str(ex),
            )

    def read_one_task_type(
        self, model_id: int, request: Request, is_include_task_calendars: bool
    ) -> TaskTypeResponse:
        try:
            data_model: TaskTypeModel = super().read_one(model_id)
            if data_model:
                schema_model: TaskTypeSchema = _convert_model_to_schema(
                    data_model, is_include_task_calendars
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def read_all_task_types(
        self, request: Request, is_include_task_calendars: bool
    ) -> TaskTypeResponse:
        try:
            data_models: List[TaskTypeModel] = super().read_all()
            schema_models: List[TaskTypeSchema] = [
                _convert_model_to_schema(c_m, is_include_task_calendars)
                for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving TaskTypes. Please Try Again!!!",
                str(ex),
            )

    def update_one_task_type(
        self, model_id: int, request: Request, request_object: TaskTypeRequest
    ) -> TaskTypeResponse:
        task_type_response = self.read_one_task_type(model_id, request, False)

        if not (task_type_response and task_type_response.task_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: TaskTypeModel = copy_objects(request_object, TaskTypeModel)
            data_model = super().update(model_id, data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Updating By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def delete_one_task_type(self, model_id: int, request: Request) -> TaskTypeResponse:
        task_type_response = self.read_one_task_type(model_id, request, False)

        if not (task_type_response and task_type_response.task_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return TaskTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_task_type_service(db_session: Session) -> TaskTypeService:
    return TaskTypeService(db_session)


def get_response_single(single: TaskTypeSchema) -> TaskTypeResponse:
    return TaskTypeResponse(task_types=[single])


def get_response_multiple(multiple: list[TaskTypeSchema]) -> TaskTypeResponse:
    return TaskTypeResponse(task_types=multiple)


def _convert_model_to_schema(
    data_model: TaskTypeModel, is_include_task_calendars: bool = False
) -> TaskTypeSchema:
    data_schema = TaskTypeSchema(
        name=data_model.name,
        description=data_model.description,
    )
    if is_include_task_calendars:
        data_schema.task_calendars = data_model.task_calendars
    return data_schema
