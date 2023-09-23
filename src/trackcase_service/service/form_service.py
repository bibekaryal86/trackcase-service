from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Form as FormModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import Form as FormSchema
from .schemas import FormRequest, FormResponse


class FormService(CrudService):
    def __init__(self, db_session: Session):
        super(FormService, self).__init__(db_session, FormModel)

    def create_one_form(
        self, request: Request, request_object: FormRequest
    ) -> FormResponse:
        try:
            data_model: FormModel = copy_objects(request_object, FormModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting Form. Please Try Again!!!",
                str(ex),
            )

    def read_one_form(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> FormResponse:
        try:
            data_model: FormModel = super().read_one(model_id)
            if data_model:
                schema_model: FormSchema = _convert_model_to_schema(
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

    def read_all_forms(self, request: Request, is_include_extras: bool) -> FormResponse:
        try:
            data_models: List[FormModel] = super().read_all()
            schema_models: List[FormSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving Forms. Please Try Again!!!",
                str(ex),
            )

    def update_one_form(
        self, model_id: int, request: Request, request_object: FormRequest
    ) -> FormResponse:
        form_response = self.read_one_form(model_id, request, False)

        if not (form_response and form_response.forms):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: FormModel = copy_objects(request_object, FormModel)
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

    def delete_one_form(self, model_id: int, request: Request) -> FormResponse:
        form_response = self.read_one_form(model_id, request, False)

        if not (form_response and form_response.forms):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return FormResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_form_service(db_session: Session) -> FormService:
    return FormService(db_session)


def get_response_single(single: FormSchema) -> FormResponse:
    return FormResponse(forms=[single])


def get_response_multiple(multiple: list[FormSchema]) -> FormResponse:
    return FormResponse(forms=multiple)


def _convert_model_to_schema(
    data_model: FormModel, is_include_extras: bool = False
) -> FormSchema:
    data_schema = FormSchema(
        form_type_id=data_model.form_type_id,
        form_status_id=data_model.form_status_id,
        court_case_id=data_model.court_case_id,
        submit_date=data_model.submit_date,
        receipt_date=data_model.receipt_date,
        rfe_date=data_model.rfe_date,
        rfe_submit_date=data_model.rfe_submit_date,
        decision_date=data_model.decision_date,
        task_calendar_id=data_model.task_calendar_id,
    )
    if is_include_extras:
        data_schema.form_status = data_model.form_status
        data_schema.form_type = data_model.form_type
        data_schema.task_calendar = data_model.task_calendar
        data_schema.court_case = data_model.court_case
        data_schema.cash_collections = data_model.cash_collections
    return data_schema
