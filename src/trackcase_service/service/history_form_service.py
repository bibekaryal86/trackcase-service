from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import HistoryForm as HistoryFormModel
from src.trackcase_service.utils.commons import (
    copy_objects,
    get_err_msg,
    raise_http_exception,
)

from .schemas import HistoryForm as HistoryFormSchema
from .schemas import HistoryFormRequest, HistoryFormResponse


class HistoryFormService(CrudService):
    def __init__(self, db_session: Session):
        super(HistoryFormService, self).__init__(db_session, HistoryFormModel)

    def create_one_history_form(
        self,
        request: Request,
        request_object: HistoryFormRequest,
        is_form_service_request: bool = False,
    ) -> HistoryFormResponse:
        try:
            data_model: HistoryFormModel = copy_objects(
                request_object, HistoryFormModel
            )
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            if is_form_service_request:
                raise Exception(
                    "Form Action Successful! BUT!! "
                    "Something went wrong inserting FormHistory!!!"
                )
            else:
                raise_http_exception(
                    request,
                    HTTPStatus.SERVICE_UNAVAILABLE,
                    get_err_msg(
                        "Error Inserting HistoryForm. Please Try Again!!!", str(ex)
                    ),
                )

    def read_one_history_form(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> HistoryFormResponse:
        try:
            data_model: HistoryFormModel = super().read_one(model_id)
            if data_model:
                schema_model: HistoryFormSchema = _convert_model_to_schema(
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

    def read_all_history_forms(
        self, request: Request, is_include_extras: bool
    ) -> HistoryFormResponse:
        try:
            data_models: List[HistoryFormModel] = super().read_all()
            schema_models: List[HistoryFormSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving HistoryForms. Please Try Again!!!", str(ex)
                ),
            )

    def read_many_history_forms_by_form_id(
        self, form_id: int, request: Request, is_include_extras: bool
    ) -> HistoryFormResponse:
        try:
            data_models: List[HistoryFormModel] = super().read_many(
                **{"form_id": form_id}
            )
            schema_models: List[HistoryFormSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving HistoryForms by form_id: "
                    f"{form_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def update_one_history_form(
        self, model_id: int, request: Request, request_object: HistoryFormRequest
    ) -> HistoryFormResponse:
        history_form_response = self.read_one_history_form(model_id, request, False)

        if not (history_form_response and history_form_response.history_forms):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: HistoryFormModel = copy_objects(
                request_object, HistoryFormModel
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

    def delete_one_history_form(
        self, model_id: int, request: Request
    ) -> HistoryFormResponse:
        history_form_response = self.read_one_history_form(model_id, request, False)

        if not (history_form_response and history_form_response.history_forms):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return HistoryFormResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )


def get_history_form_service(db_session: Session) -> HistoryFormService:
    return HistoryFormService(db_session)


def get_response_single(single: HistoryFormSchema) -> HistoryFormResponse:
    return HistoryFormResponse(history_forms=[single])


def get_response_multiple(multiple: list[HistoryFormSchema]) -> HistoryFormResponse:
    return HistoryFormResponse(history_forms=multiple)


def _convert_model_to_schema(
    data_model: HistoryFormModel, is_include_extras: bool = False
) -> HistoryFormSchema:
    data_schema = HistoryFormSchema(
        id=data_model.id,
        created=data_model.created,
        modified=data_model.modified,
        user_name=data_model.user_name,
        form_id=data_model.form_id,
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
