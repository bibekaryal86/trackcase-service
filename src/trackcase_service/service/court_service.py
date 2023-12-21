from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Court as CourtModel
from src.trackcase_service.db.models import HistoryCourt as HistoryCourtModel
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import Court as CourtSchema
from src.trackcase_service.service.schemas import CourtRequest, CourtResponse
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_court_model_to_schema,
    convert_request_schema_to_model,
)


class CourtService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtService, self).__init__(db_session, CourtModel)

    def create_one_court(
        self, request: Request, request_object: CourtRequest
    ) -> CourtResponse:
        try:
            data_model: CourtModel = convert_request_schema_to_model(
                request_object, CourtModel
            )
            data_model = super().create(data_model)
            _create_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_court_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting Court. Please Try Again!!!", str(ex)),
            )

    def read_one_court(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> CourtResponse:
        try:
            data_model: CourtModel = super().read_one(model_id)
            if data_model:
                schema_model: CourtSchema = convert_court_model_to_schema(
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
                    f"Error Retrieving Court By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_courts(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> CourtResponse:
        try:
            data_models: List[CourtModel] = super().read_all(
                sort_direction="asc", sort_by="name"
            )
            schema_models: List[CourtSchema] = [
                convert_court_model_to_schema(
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
                get_err_msg("Error Retrieving Courts. Please Try Again!!!", str(ex)),
            )

    def update_one_court(
        self, model_id: int, request: Request, request_object: CourtRequest
    ) -> CourtResponse:
        court_response = self.read_one_court(model_id, request)

        if not (court_response and court_response.courts):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Court Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CourtModel = convert_request_schema_to_model(
                request_object, CourtModel
            )
            data_model = super().update(model_id, data_model)
            _create_history(self.db_session, request, model_id, request_object)
            schema_model = convert_court_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating Court By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_court(self, model_id: int, request: Request) -> CourtResponse:
        court_response = self.read_one_court(model_id, request)

        if not (court_response and court_response.courts):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Court Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            _create_history(self.db_session, request, model_id, is_delete=True)
            return CourtResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Court By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_court_service(db_session: Session) -> CourtService:
    return CourtService(db_session)


def get_response_single(single: CourtSchema) -> CourtResponse:
    return CourtResponse(courts=[single])


def get_response_multiple(multiple: list[CourtSchema]) -> CourtResponse:
    return CourtResponse(courts=multiple)


def _create_history(
    db_session: Session,
    request: Request,
    court_id: int,
    request_object: CourtRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryCourtModel)
    if is_delete:
        history_service.add_to_history_for_delete(
            request,
            HistoryCourtModel.__tablename__,
            "court_id",
            court_id,
            "Court",
            "HistoryCourt",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "court_id",
            court_id,
            "Court",
            "HistoryCourt",
        )
