from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import FormStatus as FormStatusModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import FormStatus as FormStatusSchema
from .schemas import FormStatusRequest, FormStatusResponse


class FormStatusService(CrudService):
    def __init__(self, db_session: Session):
        super(FormStatusService, self).__init__(db_session, FormStatusModel)

    def create_one_form_status(
        self, request: Request, request_object: FormStatusRequest
    ) -> FormStatusResponse:
        try:
            data_model: FormStatusModel = copy_objects(request_object, FormStatusModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting FormStatus. Please Try Again!!!",
                str(ex),
            )

    def read_one_form_status(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> FormStatusResponse:
        try:
            data_model: FormStatusModel = super().read_one(model_id)
            if data_model:
                schema_model: FormStatusSchema = _convert_model_to_schema(
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

    def read_all_form_statuses(
        self, request: Request, is_include_extras: bool
    ) -> FormStatusResponse:
        try:
            data_models: List[FormStatusModel] = super().read_all()
            schema_models: List[FormStatusSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving FormStatuses. Please Try Again!!!",
                str(ex),
            )

    def update_one_form_status(
        self, model_id: int, request: Request, request_object: FormStatusRequest
    ) -> FormStatusResponse:
        form_status_response = self.read_one_form_status(model_id, request, False)

        if not (form_status_response and form_status_response.form_statuses):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: FormStatusModel = copy_objects(request_object, FormStatusModel)
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

    def delete_one_form_status(
        self, model_id: int, request: Request
    ) -> FormStatusResponse:
        form_status_response = self.read_one_form_status(model_id, request, False)

        if not (form_status_response and form_status_response.form_statuses):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return FormStatusResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_form_status_service(db_session: Session) -> FormStatusService:
    return FormStatusService(db_session)


def get_response_single(single: FormStatusSchema) -> FormStatusResponse:
    return FormStatusResponse(form_statuses=[single])


def get_response_multiple(multiple: list[FormStatusSchema]) -> FormStatusResponse:
    return FormStatusResponse(form_statuses=multiple)


def _convert_model_to_schema(
    data_model: FormStatusModel, is_include_extras: bool = False
) -> FormStatusSchema:
    data_schema = FormStatusSchema(
        name=data_model.name,
        description=data_model.description,
    )
    if is_include_extras:
        data_schema.forms = data_model.forms
    return data_schema
