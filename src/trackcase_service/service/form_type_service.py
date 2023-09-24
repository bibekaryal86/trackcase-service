from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import FormType as FormTypeModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import FormType as FormTypeSchema
from .schemas import FormTypeRequest, FormTypeResponse


class FormTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(FormTypeService, self).__init__(db_session, FormTypeModel)

    def create_one_form_type(
        self, request: Request, request_object: FormTypeRequest
    ) -> FormTypeResponse:
        try:
            data_model: FormTypeModel = copy_objects(request_object, FormTypeModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting FormType. Please Try Again!!!",
                str(ex),
            )

    def read_one_form_type(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> FormTypeResponse:
        try:
            data_model: FormTypeModel = super().read_one(model_id)
            if data_model:
                schema_model: FormTypeSchema = _convert_model_to_schema(
                    data_model, is_include_extras
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def read_all_form_types(
        self, request: Request, is_include_extras: bool
    ) -> FormTypeResponse:
        try:
            data_models: List[FormTypeModel] = super().read_all()
            schema_models: List[FormTypeSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving FormTypes. Please Try Again!!!",
                str(ex),
            )

    def update_one_form_type(
        self, model_id: int, request: Request, request_object: FormTypeRequest
    ) -> FormTypeResponse:
        form_type_response = self.read_one_form_type(model_id, request, False)

        if not (form_type_response and form_type_response.form_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: FormTypeModel = copy_objects(request_object, FormTypeModel)
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

    def delete_one_form_type(self, model_id: int, request: Request) -> FormTypeResponse:
        form_type_response = self.read_one_form_type(model_id, request, False)

        if not (form_type_response and form_type_response.form_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return FormTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_form_type_service(db_session: Session) -> FormTypeService:
    return FormTypeService(db_session)


def get_response_single(single: FormTypeSchema) -> FormTypeResponse:
    return FormTypeResponse(form_types=[single])


def get_response_multiple(multiple: list[FormTypeSchema]) -> FormTypeResponse:
    return FormTypeResponse(form_types=multiple)


def _convert_model_to_schema(
    data_model: FormTypeModel, is_include_extras: bool = False
) -> FormTypeSchema:
    data_schema = FormTypeSchema(
        id=data_model.id,
        created=data_model.created,
        modified=data_model.modified,
        name=data_model.name,
        description=data_model.description,
    )
    if is_include_extras:
        data_schema.forms = data_model.forms
    return data_schema
