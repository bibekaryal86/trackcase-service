from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import HearingType as HearingTypeModel
from src.trackcase_service.service.schemas import HearingType as HearingTypeSchema
from src.trackcase_service.service.schemas import (
    HearingTypeRequest,
    HearingTypeResponse,
)
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_hearing_type_model_to_schema,
    convert_request_schema_to_model,
)


class HearingTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(HearingTypeService, self).__init__(db_session, HearingTypeModel)

    def create_one_hearing_type(
        self, request: Request, request_object: HearingTypeRequest
    ) -> HearingTypeResponse:
        try:
            data_model: HearingTypeModel = convert_request_schema_to_model(
                request_object, HearingTypeModel
            )
            data_model = super().create(data_model)
            schema_model = convert_hearing_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting HearingType. Please Try Again!!!", str(ex)
                ),
            )

    def read_one_hearing_type(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> HearingTypeResponse:
        try:
            data_model: HearingTypeModel = super().read_one(model_id)
            if data_model:
                schema_model: HearingTypeSchema = convert_hearing_type_model_to_schema(
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
                    f"Error Retrieving HearingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )

    def read_all_hearing_types(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> HearingTypeResponse:
        try:
            sort_config = {"name": "asc"}
            data_models: List[HearingTypeModel] = super().read_all(sort_config)
            schema_models: List[HearingTypeSchema] = [
                convert_hearing_type_model_to_schema(
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
                get_err_msg(
                    "Error Retrieving HearingTypes. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_hearing_type(
        self, model_id: int, request: Request, request_object: HearingTypeRequest
    ) -> HearingTypeResponse:
        hearing_type_response = self.read_one_hearing_type(model_id, request)

        if not (hearing_type_response and hearing_type_response.hearing_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"HearingType Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: HearingTypeModel = convert_request_schema_to_model(
                request_object, HearingTypeModel
            )
            data_model = super().update(model_id, data_model)
            schema_model = convert_hearing_type_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating HearingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )

    def delete_one_hearing_type(
        self, model_id: int, request: Request
    ) -> HearingTypeResponse:
        hearing_type_response = self.read_one_hearing_type(model_id, request)

        if not (hearing_type_response and hearing_type_response.hearing_types):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"HearingType Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return HearingTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting HearingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )


def get_hearing_type_service(db_session: Session) -> HearingTypeService:
    return HearingTypeService(db_session)


def get_response_single(single: HearingTypeSchema) -> HearingTypeResponse:
    return HearingTypeResponse(hearing_types=[single])


def get_response_multiple(multiple: list[HearingTypeSchema]) -> HearingTypeResponse:
    return HearingTypeResponse(hearing_types=multiple)
