from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Form as FormModel
from src.trackcase_service.db.models import HistoryForm as HistoryFormModel
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import Form as FormSchema
from src.trackcase_service.service.schemas import FormRequest, FormResponse
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_form_model_to_schema,
    convert_request_schema_to_model,
)


class FormService(CrudService):
    def __init__(self, db_session: Session):
        super(FormService, self).__init__(db_session, FormModel)

    def create_one_form(
        self, request: Request, request_object: FormRequest
    ) -> FormResponse:
        try:
            data_model: FormModel = convert_request_schema_to_model(
                request_object, FormModel
            )
            data_model = super().create(data_model)
            _create_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_form_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting Form. Please Try Again!!!", str(ex)),
            )

    def read_one_form(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> FormResponse:
        try:
            data_model: FormModel = super().read_one(model_id)
            if data_model:
                schema_model: FormSchema = convert_form_model_to_schema(
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
                    f"Error Retrieving Form By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_forms(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> FormResponse:
        try:
            data_models: List[FormModel] = super().read_all(
                sort_direction="desc", sort_by="submit_date"
            )
            schema_models: List[FormSchema] = [
                convert_form_model_to_schema(
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
                get_err_msg("Error Retrieving Forms. Please Try Again!!!", str(ex)),
            )

    def update_one_form(
        self, model_id: int, request: Request, request_object: FormRequest
    ) -> FormResponse:
        form_response = self.read_one_form(model_id, request)

        if not (form_response and form_response.forms):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Form Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: FormModel = convert_request_schema_to_model(
                request_object, FormModel
            )
            data_model = super().update(model_id, data_model)
            _create_history(self.db_session, request, model_id, request_object)
            schema_model = convert_form_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating Form By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_form(self, model_id: int, request: Request) -> FormResponse:
        form_response = self.read_one_form(model_id, request)

        if not (form_response and form_response.forms):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Form Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            _create_history(self.db_session, request, model_id, is_delete=True)
            return FormResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Form By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_form_service(db_session: Session) -> FormService:
    return FormService(db_session)


def get_response_single(single: FormSchema) -> FormResponse:
    return FormResponse(forms=[single])


def get_response_multiple(multiple: list[FormSchema]) -> FormResponse:
    return FormResponse(forms=multiple)


def _create_history(
    db_session: Session,
    request: Request,
    form_id: int,
    request_object: FormRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryFormModel)
    if is_delete:
        history_service.add_to_history_for_delete(
            request,
            HistoryFormModel.__tablename__,
            "form_id",
            form_id,
            "Form",
            "HistoryForm",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "form_id",
            form_id,
            "Form",
            "HistoryForm",
        )
