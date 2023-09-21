from typing import List
from http import HTTPStatus
from sqlalchemy.orm import Session
from fastapi import Request
from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Court as CourtModel
from src.trackcase_service.utils.commons import (
    copy_objects,
    raise_http_exception,
)

from .schemas import Court as CourtSchema, CourtRequest, CourtResponse


class CourtService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtService, self).__init__(db_session, CourtModel)

    def read_one_court(self, model_id: int, request: Request) -> CourtResponse:
        try:
            court_model: CourtModel = super().read_one(model_id)
            if court_model:
                court_schema: CourtSchema = _convert_model_to_schema(court_model)
                return get_response_single(court_schema)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def read_all_courts(self, request: Request) -> CourtResponse:
        try:
            court_models: List[CourtModel] = super().read_all()
            court_schemas: List[CourtSchema] = [_convert_model_to_schema(c_m) for c_m in court_models]
            return get_response_multiple(court_schemas)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving Courts. Please Try Again!!!",
                str(ex),
            )

    def create_one_court(self, request: Request, request_object: CourtRequest) -> CourtModel:
        try:
            court_model: CourtModel = copy_objects(request_object, CourtModel)
            return super().create(court_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting Court. Please Try Again!!!",
                str(ex),
            )

    def delete_one_court(self, model_id: int, request: Request) -> CourtResponse:
        try:
            deleted = super().delete(model_id)
            if deleted:
                return CourtResponse(delete_count=1)
            else:
                return CourtResponse(delete_count=0)
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


def _convert_model_to_schema(court_model: CourtModel) -> CourtSchema:
    court_schema = CourtSchema(name=court_model.name, address=court_model.address,
                               dhs_address=court_model.dhs_address)
    court_schema = copy_objects(court_model, CourtSchema, court_schema)
    return court_schema
