from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CourtCase as CourtCaseModel
from src.trackcase_service.utils.commons import (
    copy_objects,
    get_err_msg,
    raise_http_exception,
)

from .schemas import CourtCase as CourtCaseSchema
from .schemas import CourtCaseRequest, CourtCaseResponse


class CourtCaseService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtCaseService, self).__init__(db_session, CourtCaseModel)

    def create_one_court_case(
        self, request: Request, request_object: CourtCaseRequest
    ) -> CourtCaseResponse:
        try:
            data_model: CourtCaseModel = copy_objects(request_object, CourtCaseModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting CourtCase. Please Try Again!!!", str(ex)),
            )

    def read_one_court_case(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> CourtCaseResponse:
        try:
            data_model: CourtCaseModel = super().read_one(model_id)
            if data_model:
                schema_model: CourtCaseSchema = _convert_model_to_schema(
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

    def read_all_court_cases(
        self, request: Request, is_include_extras: bool
    ) -> CourtCaseResponse:
        try:
            data_models: List[CourtCaseModel] = super().read_all()
            schema_models: List[CourtCaseSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving CourtCases. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_court_case(
        self, model_id: int, request: Request, request_object: CourtCaseRequest
    ) -> CourtCaseResponse:
        court_case_response = self.read_one_court_case(model_id, request, False)

        if not (court_case_response and court_case_response.court_cases):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CourtCaseModel = copy_objects(request_object, CourtCaseModel)
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

    def delete_one_court_case(
        self, model_id: int, request: Request
    ) -> CourtCaseResponse:
        court_case_response = self.read_one_court_case(model_id, request, False)

        if not (court_case_response and court_case_response.court_cases):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CourtCaseResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )


def get_court_case_service(db_session: Session) -> CourtCaseService:
    return CourtCaseService(db_session)


def get_response_single(single: CourtCaseSchema) -> CourtCaseResponse:
    return CourtCaseResponse(court_cases=[single])


def get_response_multiple(multiple: list[CourtCaseSchema]) -> CourtCaseResponse:
    return CourtCaseResponse(court_cases=multiple)


def _convert_model_to_schema(
    data_model: CourtCaseModel, is_include_extras: bool = False
) -> CourtCaseSchema:
    data_schema = CourtCaseSchema(
        id=data_model.id,
        created=data_model.created,
        modified=data_model.modified,
        case_type_id=data_model.case_type_id,
        client_id=data_model.client_id,
    )
    if is_include_extras:
        data_schema.case_type = data_model.case_type
        data_schema.client = data_model.client
        data_schema.forms = data_model.forms
        data_schema.cash_collections = data_model.cash_collections
        data_schema.case_collections = data_model.case_collections
        data_schema.hearing_calendars = data_model.hearing_calendars
        data_schema.task_calendars = data_model.task_calendars
    return data_schema
