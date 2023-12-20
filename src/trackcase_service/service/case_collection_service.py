from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CaseCollection as CaseCollectionModel
from src.trackcase_service.db.models import (
    HistoryCaseCollection as HistoryCaseCollectionModel,
)
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import CaseCollection as CaseCollectionSchema
from src.trackcase_service.service.schemas import (
    CaseCollectionRequest,
    CaseCollectionResponse,
    CaseCollectionRetrieveRequest,
)
from src.trackcase_service.service.schemas import (
    HistoryCaseCollection as HistoryCaseCollectionSchema,
)
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_case_collection_model_to_schema,
    convert_request_schema_to_model,
)


class CaseCollectionService(CrudService):
    def __init__(self, db_session: Session):
        super(CaseCollectionService, self).__init__(db_session, CaseCollectionModel)

    def create_one_case_collection(
        self, request: Request, request_object: CaseCollectionRequest
    ) -> CaseCollectionResponse:
        try:
            data_model: CaseCollectionModel = convert_request_schema_to_model(
                request_object, CaseCollectionModel
            )
            data_model = super().create(data_model)
            _create_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_case_collection_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting CaseCollection. Please Try Again!!!", str(ex)
                ),
            )

    def read_one_case_collection(
        self,
        model_id: int,
        request: Request,
        is_include_extra_objects: bool = False,
        is_include_extra_lists: bool = False,
        is_include_history: bool = False,
    ) -> CaseCollectionResponse:
        try:
            data_model: CaseCollectionModel = super().read_one(model_id)
            if data_model:
                schema_model: CaseCollectionSchema = (
                    convert_case_collection_model_to_schema(
                        data_model,
                        is_include_extra_objects,
                        is_include_extra_lists,
                        is_include_history,
                    )
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving CaseCollection By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_case_collections(
        self,
        request: Request,
        is_include_extra_objects: bool = False,
        is_include_extra_lists: bool = False,
        is_include_history: bool = False,
    ) -> CaseCollectionResponse:
        try:
            data_models: List[CaseCollectionModel] = super().read_all(
                sort_direction="desc", sort_by="quote_date"
            )
            schema_models: List[CaseCollectionSchema] = [
                convert_case_collection_model_to_schema(
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
                get_err_msg(
                    "Error Retrieving CaseCollections. Please Try Again!!!", str(ex)
                ),
            )

    def read_many_case_collections(
        self,
        request: Request,
        case_collection_retrieve_request: CaseCollectionRetrieveRequest,
        is_include_extra_objects: bool = False,
        is_include_extra_lists: bool = False,
        is_include_history: bool = False,
    ):
        filters = case_collection_retrieve_request.to_dict()

        if filters:
            data_models: List[CaseCollectionModel] = super().read_many(
                sort_direction="desc", sort_by="quote_date", **filters
            )
            schema_models: List[CaseCollectionSchema] = [
                convert_case_collection_model_to_schema(
                    data_model,
                    is_include_extra_objects,
                    is_include_extra_lists,
                    is_include_history,
                )
                for data_model in data_models
            ]
            return get_response_multiple(schema_models)
        else:
            self.read_all_case_collections(
                request,
                is_include_extra_objects,
                is_include_extra_lists,
                is_include_history,
            )

    def update_one_case_collection(
        self, model_id: int, request: Request, request_object: CaseCollectionRequest
    ) -> CaseCollectionResponse:
        case_collection_response = self.read_one_case_collection(model_id, request)

        if not (case_collection_response and case_collection_response.case_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CaseCollection Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CaseCollectionModel = convert_request_schema_to_model(
                request_object, CaseCollectionModel
            )
            data_model = super().update(model_id, data_model)
            _create_history(self.db_session, request, model_id, request_object)
            schema_model = convert_case_collection_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating CaseCollection By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_case_collection(
        self, model_id: int, request: Request
    ) -> CaseCollectionResponse:
        case_collection_response = self.read_one_case_collection(
            model_id,
            request,
        )

        if not (case_collection_response and case_collection_response.case_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CaseCollection Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            _create_history(self.db_session, request, model_id, is_delete=True)
            return CaseCollectionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting CaseCollection By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_case_collection_service(db_session: Session) -> CaseCollectionService:
    return CaseCollectionService(db_session)


def get_response_single(single: CaseCollectionSchema) -> CaseCollectionResponse:
    return CaseCollectionResponse(case_collections=[single])


def get_response_multiple(
    multiple: list[CaseCollectionSchema],
) -> CaseCollectionResponse:
    return CaseCollectionResponse(case_collections=multiple)


def _create_history(
    db_session: Session,
    request: Request,
    case_collection_id: int,
    request_object: CaseCollectionRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryCaseCollectionModel)
    if is_delete:
        history_service.add_to_history_for_delete(
            request,
            HistoryCaseCollectionModel.__tablename__,
            "case_collection_id",
            case_collection_id,
            "CaseCollection",
            "HistoryCaseCollection",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            HistoryCaseCollectionSchema,
            "case_collection_id",
            case_collection_id,
            "CaseCollection",
            "HistoryCaseCollection",
        )