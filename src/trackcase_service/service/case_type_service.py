from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CaseType as CaseTypeModel
from src.trackcase_service.service.schemas import CaseType as CaseTypeSchema
from src.trackcase_service.service.schemas import CaseTypeRequest, CaseTypeResponse
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_case_type_model_to_schema,
    convert_request_schema_to_model,
)


class CaseTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(CaseTypeService, self).__init__(db_session, CaseTypeModel)

    def create_one_case_type(
        self, request: Request, request_object: CaseTypeRequest
    ) -> CaseTypeResponse:
        try:
            data_model: CaseTypeModel = convert_request_schema_to_model(
                request_object, CaseTypeModel
            )
            data_model = super().create(data_model)
            schema_model = convert_case_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting CaseType. Please Try Again!!!", str(ex)),
            )

    def read_one_case_type(
        self,
        model_id: int,
        request: Request,
        is_include_extra_objects: bool = False,
        is_include_extra_lists: bool = False,
        is_include_history: bool = False,
    ) -> CaseTypeResponse:
        try:
            data_model: CaseTypeModel = super().read_one(model_id)
            if data_model:
                schema_model: CaseTypeSchema = convert_case_type_model_to_schema(
                    data_model,
                    is_include_extra_objects,
                    is_include_extra_lists,
                    is_include_history,
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving CaseType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_case_types(
        self,
        request: Request,
        is_include_extra_objects: bool = False,
        is_include_extra_lists: bool = False,
        is_include_history: bool = False,
    ) -> CaseTypeResponse:
        try:
            data_models: List[CaseTypeModel] = super().read_all(
                sort_direction="asc", sort_by="name"
            )
            schema_models: List[CaseTypeSchema] = [
                convert_case_type_model_to_schema(
                    data_model,
                    is_include_extra_objects,
                    is_include_extra_lists,
                    is_include_history,
                )
                for data_model in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving CaseTypes. Please Try Again!!!", str(ex)),
            )

    def update_one_case_type(
        self, model_id: int, request: Request, request_object: CaseTypeRequest
    ) -> CaseTypeResponse:
        case_type_response = self.read_one_case_type(model_id, request)

        if not (case_type_response and case_type_response.case_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CaseType Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CaseTypeModel = convert_request_schema_to_model(
                request_object, CaseTypeModel
            )
            data_model = super().update(model_id, data_model)
            schema_model = convert_case_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating CaseType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_case_type(self, model_id: int, request: Request) -> CaseTypeResponse:
        case_type_response = self.read_one_case_type(model_id, request)

        if not (case_type_response and case_type_response.case_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CaseType Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CaseTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting CaseType By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_case_type_service(db_session: Session) -> CaseTypeService:
    return CaseTypeService(db_session)


def get_response_single(single: CaseTypeSchema) -> CaseTypeResponse:
    return CaseTypeResponse(case_types=[single])


def get_response_multiple(multiple: list[CaseTypeSchema]) -> CaseTypeResponse:
    return CaseTypeResponse(case_types=multiple)
