from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CourtCase as CourtCaseModel
from src.trackcase_service.db.models import HistoryCourtCase as HistoryCourtCaseModel
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import CourtCase as CourtCaseSchema
from src.trackcase_service.service.schemas import CourtCaseRequest, CourtCaseResponse
from src.trackcase_service.service.schemas import (
    HistoryCourtCase as HistoryCourtCaseSchema,
)
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_court_case_model_to_schema,
    convert_request_schema_to_model,
)


class CourtCaseService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtCaseService, self).__init__(db_session, CourtCaseModel)

    def create_one_court_case(
        self, request: Request, request_object: CourtCaseRequest
    ) -> CourtCaseResponse:
        try:
            data_model: CourtCaseModel = convert_request_schema_to_model(
                request_object, CourtCaseModel
            )
            data_model = super().create(data_model)
            _create_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_court_case_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting CourtCase. Please Try Again!!!", str(ex)),
            )

    def read_one_court_case(
        self,
        model_id: int,
        request: Request,
        is_include_extra_objects: bool = False,
        is_include_extra_lists: bool = False,
        is_include_history: bool = False,
    ) -> CourtCaseResponse:
        try:
            data_model: CourtCaseModel = super().read_one(model_id)
            if data_model:
                schema_model: CourtCaseSchema = convert_court_case_model_to_schema(
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
                    f"Error Retrieving CourtCase By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_court_cases(
        self,
        request: Request,
        is_include_extra_objects: bool = False,
        is_include_extra_lists: bool = False,
        is_include_history: bool = False,
    ) -> CourtCaseResponse:
        try:
            data_models: List[CourtCaseModel] = super().read_all()
            schema_models: List[CourtCaseSchema] = [
                convert_court_case_model_to_schema(
                    data_model,
                    is_include_extra_objects,
                    is_include_extra_lists,
                    is_include_history,
                )
                for data_model in data_models
            ]
            sorted_schema_models: List[
                CourtCaseSchema
            ] = _sort_court_case_by_client_name(schema_models)
            return get_response_multiple(sorted_schema_models)
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
        court_case_response = self.read_one_court_case(model_id, request)

        if not (court_case_response and court_case_response.court_cases):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CourtCase Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CourtCaseModel = convert_request_schema_to_model(
                request_object, CourtCaseModel
            )
            data_model = super().update(model_id, data_model)
            _create_history(self.db_session, request, model_id, request_object)
            schema_model = convert_court_case_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating CourtCase By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_court_case(
        self, model_id: int, request: Request
    ) -> CourtCaseResponse:
        court_case_response = self.read_one_court_case(model_id, request)

        if not (court_case_response and court_case_response.court_cases):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CourtCase Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            _create_history(self.db_session, request, model_id, is_delete=True)
            return CourtCaseResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting CourtCase By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_court_case_service(db_session: Session) -> CourtCaseService:
    return CourtCaseService(db_session)


def get_response_single(single: CourtCaseSchema) -> CourtCaseResponse:
    return CourtCaseResponse(court_cases=[single])


def get_response_multiple(multiple: list[CourtCaseSchema]) -> CourtCaseResponse:
    return CourtCaseResponse(court_cases=multiple)


def _sort_court_case_by_client_name(
    court_cases: List[CourtCaseSchema],
) -> List[CourtCaseSchema]:
    return sorted(
        court_cases,
        key=lambda x: x.client.name if (x.client and x.client.name) else "",
    )


def _create_history(
    db_session: Session,
    request: Request,
    court_case_id: int,
    request_object: CourtCaseRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryCourtCaseModel)
    if is_delete:
        history_service.add_to_history_for_delete(
            request,
            HistoryCourtCaseModel.__tablename__,
            "court_case_id",
            court_case_id,
            "CourtCase",
            "HistoryCourtCase",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            HistoryCourtCaseSchema,
            "court_case_id",
            court_case_id,
            "CourtCase",
            "HistoryCourtCase",
        )
