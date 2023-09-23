from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CaseType as CaseTypeModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import CaseType as CaseTypeSchema
from .schemas import CaseTypeRequest, CaseTypeResponse


class CaseTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(CaseTypeService, self).__init__(db_session, CaseTypeModel)

    def create_one_case_type(
        self, request: Request, request_object: CaseTypeRequest
    ) -> CaseTypeResponse:
        try:
            data_model: CaseTypeModel = copy_objects(request_object, CaseTypeModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting CaseType. Please Try Again!!!",
                str(ex),
            )

    def read_one_case_type(
        self, model_id: int, request: Request, is_include_court_cases: bool
    ) -> CaseTypeResponse:
        try:
            data_model: CaseTypeModel = super().read_one(model_id)
            if data_model:
                schema_model: CaseTypeSchema = _convert_model_to_schema(
                    data_model, is_include_court_cases
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def read_all_case_types(
        self, request: Request, is_include_court_cases: bool
    ) -> CaseTypeResponse:
        try:
            data_models: List[CaseTypeModel] = super().read_all()
            schema_models: List[CaseTypeSchema] = [
                _convert_model_to_schema(c_m, is_include_court_cases) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving CaseTypes. Please Try Again!!!",
                str(ex),
            )

    def update_one_case_type(
        self, model_id: int, request: Request, request_object: CaseTypeRequest
    ) -> CaseTypeResponse:
        case_type_response = self.read_one_case_type(model_id, request, False)

        if not (case_type_response and case_type_response.case_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CaseTypeModel = copy_objects(request_object, CaseTypeModel)
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

    def delete_one_case_type(self, model_id: int, request: Request) -> CaseTypeResponse:
        case_type_response = self.read_one_case_type(model_id, request, False)

        if not (case_type_response and case_type_response.case_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CaseTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_case_type_service(db_session: Session) -> CaseTypeService:
    return CaseTypeService(db_session)


def get_response_single(single: CaseTypeSchema) -> CaseTypeResponse:
    return CaseTypeResponse(case_types=[single])


def get_response_multiple(multiple: list[CaseTypeSchema]) -> CaseTypeResponse:
    return CaseTypeResponse(case_types=multiple)


def _convert_model_to_schema(
    data_model: CaseTypeModel, is_include_court_cases: bool = False
) -> CaseTypeSchema:
    data_schema = CaseTypeSchema(
        name=data_model.name,
        description=data_model.description,
    )
    if is_include_court_cases:
        data_schema.court_cases = data_model.court_cases
    return data_schema
