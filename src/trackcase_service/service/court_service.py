from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Court as CourtModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import Court as CourtSchema, CourtRequest, CourtResponse


class CourtService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtService, self).__init__(db_session, CourtModel)

    def create_one_court(
        self, request: Request, request_object: CourtRequest
    ) -> CourtResponse:
        try:
            data_model: CourtModel = copy_objects(request_object, CourtModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting Court. Please Try Again!!!",
                str(ex),
            )

    def read_one_court(self, model_id: int, request: Request) -> CourtResponse:
        try:
            data_model: CourtModel = super().read_one(model_id)
            if data_model:
                schema_model: CourtSchema = _convert_model_to_schema(data_model)
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def read_all_courts(self, request: Request) -> CourtResponse:
        try:
            data_models: List[CourtModel] = super().read_all()
            schema_models: List[CourtSchema] = [
                _convert_model_to_schema(c_m) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving Courts. Please Try Again!!!",
                str(ex),
            )

    def update_one_court(
        self, model_id: int, request: Request, request_object: CourtRequest
    ) -> CourtResponse:
        court_response = self.read_one_court(model_id, request)

        if not (court_response and court_response.courts):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CourtModel = copy_objects(request_object, CourtModel)
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

    def delete_one_court(self, model_id: int, request: Request) -> CourtResponse:
        court_response = self.read_one_court(model_id, request)

        if not (court_response and court_response.courts):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CourtResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_court_service(db_session: Session) -> CourtService:
    return CourtService(db_session)


def get_response_single(single: CourtSchema) -> CourtResponse:
    return CourtResponse(courts=[single])


def get_response_multiple(multiple: list[CourtSchema]) -> CourtResponse:
    return CourtResponse(courts=multiple)


def _convert_model_to_schema(data_model: CourtModel) -> CourtSchema:
    data_schema = CourtSchema(
        name=data_model.name,
        address=data_model.address,
        dhs_address=data_model.dhs_address,
    )
    data_schema = copy_objects(data_model, CourtSchema, data_schema)
    return data_schema
