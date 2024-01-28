from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import FormType as FormTypeModel
from src.trackcase_service.service.schemas import FormType as FormTypeSchema
from src.trackcase_service.service.schemas import FormTypeRequest, FormTypeResponse
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_form_type_model_to_schema,
    convert_request_schema_to_model,
)


class FormTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(FormTypeService, self).__init__(db_session, FormTypeModel)

    def create_one_form_type(
        self, request: Request, request_object: FormTypeRequest
    ) -> FormTypeResponse:
        try:
            data_model: FormTypeModel = convert_request_schema_to_model(
                request_object, FormTypeModel
            )
            data_model = super().create(data_model)
            schema_model = convert_form_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting FormType. Please Try Again!!!", str(ex)),
            )

    def read_one_form_type(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> FormTypeResponse:
        try:
            data_model: FormTypeModel = super().read_one(model_id)
            if data_model:
                schema_model: FormTypeSchema = convert_form_type_model_to_schema(
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
                    f"Error Retrieving FormType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_form_types(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> FormTypeResponse:
        try:
            sort_config = {"name": "asc"}
            data_models: List[FormTypeModel] = super().read_all(sort_config)
            schema_models: List[FormTypeSchema] = [
                convert_form_type_model_to_schema(
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
                get_err_msg("Error Retrieving FormTypes. Please Try Again!!!", str(ex)),
            )

    def update_one_form_type(
        self, model_id: int, request: Request, request_object: FormTypeRequest
    ) -> FormTypeResponse:
        form_type_response = self.read_one_form_type(model_id, request)

        if not (form_type_response and form_type_response.form_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"FormType Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: FormTypeModel = convert_request_schema_to_model(
                request_object, FormTypeModel
            )
            data_model = super().update(model_id, data_model)
            schema_model = convert_form_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating FormType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_form_type(self, model_id: int, request: Request) -> FormTypeResponse:
        form_type_response = self.read_one_form_type(model_id, request)

        if not (form_type_response and form_type_response.form_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"FormType Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return FormTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting FormType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_form_type_service(db_session: Session) -> FormTypeService:
    return FormTypeService(db_session)


def get_response_single(single: FormTypeSchema) -> FormTypeResponse:
    return FormTypeResponse(form_types=[single])


def get_response_multiple(multiple: list[FormTypeSchema]) -> FormTypeResponse:
    return FormTypeResponse(form_types=multiple)
