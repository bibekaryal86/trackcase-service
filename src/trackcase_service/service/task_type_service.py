import sys
from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import TaskType as TaskTypeModel
from src.trackcase_service.service.schemas import TaskType as TaskTypeSchema
from src.trackcase_service.service.schemas import TaskTypeRequest, TaskTypeResponse
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_request_schema_to_model,
    convert_task_type_model_to_schema,
)


class TaskTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(TaskTypeService, self).__init__(db_session, TaskTypeModel)

    def create_one_task_type(
        self, request: Request, request_object: TaskTypeRequest
    ) -> TaskTypeResponse:
        try:
            data_model: TaskTypeModel = convert_request_schema_to_model(
                request_object, TaskTypeModel
            )
            data_model = super().create(data_model)
            schema_model = convert_task_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting TaskType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_one_task_type(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> TaskTypeResponse:
        try:
            data_model: TaskTypeModel = super().read_one(model_id)
            if data_model:
                schema_model: TaskTypeSchema = convert_task_type_model_to_schema(
                    data_model,
                    is_include_extra,
                    is_include_history,
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving TaskType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def read_all_task_types(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> TaskTypeResponse:
        try:
            sort_config = {"name": "asc"}
            data_models: List[TaskTypeModel] = super().read_all(sort_config)
            schema_models: List[TaskTypeSchema] = [
                convert_task_type_model_to_schema(
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
                get_err_msg("Error Retrieving TaskTypes. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def update_one_task_type(
        self, model_id: int, request: Request, request_object: TaskTypeRequest
    ) -> TaskTypeResponse:
        task_type_response = self.read_one_task_type(model_id, request)

        if not (task_type_response and task_type_response.task_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"TaskType Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: TaskTypeModel = convert_request_schema_to_model(
                request_object, TaskTypeModel
            )
            data_model = super().update(model_id, data_model)
            schema_model = convert_task_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating TaskType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_one_task_type(self, model_id: int, request: Request) -> TaskTypeResponse:
        task_type_response = self.read_one_task_type(model_id, request)

        if not (task_type_response and task_type_response.task_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"TaskType Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return TaskTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting TaskType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


def get_task_type_service(db_session: Session) -> TaskTypeService:
    return TaskTypeService(db_session)


def get_response_single(single: TaskTypeSchema) -> TaskTypeResponse:
    return TaskTypeResponse(task_types=[single])


def get_response_multiple(multiple: list[TaskTypeSchema]) -> TaskTypeResponse:
    return TaskTypeResponse(task_types=multiple)
