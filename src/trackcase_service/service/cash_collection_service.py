from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CashCollection as CashCollectionModel
from src.trackcase_service.db.models import (
    HistoryCashCollection as HistoryCashCollectionModel,
)
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import CashCollection as CashCollectionSchema
from src.trackcase_service.service.schemas import (
    CashCollectionRequest,
    CashCollectionResponse,
)
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_cash_collection_model_to_schema,
    convert_request_schema_to_model,
)


class CashCollectionService(CrudService):
    def __init__(self, db_session: Session):
        super(CashCollectionService, self).__init__(db_session, CashCollectionModel)

    def create_one_cash_collection(
        self, request: Request, request_object: CashCollectionRequest
    ) -> CashCollectionResponse:
        try:
            data_model: CashCollectionModel = convert_request_schema_to_model(
                request_object, CashCollectionModel
            )
            data_model = super().create(data_model)
            _handle_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_cash_collection_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting CashCollection. Please Try Again!!!", str(ex)
                ),
            )

    def read_one_cash_collection(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> CashCollectionResponse:
        try:
            data_model: CashCollectionModel = super().read_one(model_id)
            if data_model:
                schema_model: CashCollectionSchema = (
                    convert_cash_collection_model_to_schema(
                        data_model,
                        is_include_extra,
                        is_include_history,
                    )
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving CashCollection By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_cash_collections(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> CashCollectionResponse:
        try:
            data_models: List[CashCollectionModel] = super().read_all(
                sort_direction="desc", sort_by="collection_date"
            )
            schema_models: List[CashCollectionSchema] = [
                convert_cash_collection_model_to_schema(
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
                    "Error Retrieving CashCollections. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_cash_collection(
        self, model_id: int, request: Request, request_object: CashCollectionRequest
    ) -> CashCollectionResponse:
        cash_collection_response = self.read_one_cash_collection(model_id, request)

        if not (cash_collection_response and cash_collection_response.cash_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CashCollection Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CashCollectionModel = convert_request_schema_to_model(
                request_object, CashCollectionModel
            )
            data_model = super().update(model_id, data_model)
            _handle_history(self.db_session, request, model_id, request_object)
            schema_model = convert_cash_collection_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating CashCollection By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_cash_collection(
        self, model_id: int, request: Request
    ) -> CashCollectionResponse:
        cash_collection_response = self.read_one_cash_collection(model_id, request)

        if not (cash_collection_response and cash_collection_response.cash_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CashCollection Not Found By Id: {model_id}!!!",
            )

        try:
            _handle_history(self.db_session, request, model_id, is_delete=True)
            super().delete(model_id)
            return CashCollectionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting CashCollection By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_cash_collection_service(db_session: Session) -> CashCollectionService:
    return CashCollectionService(db_session)


def get_response_single(single: CashCollectionSchema) -> CashCollectionResponse:
    return CashCollectionResponse(cash_collections=[single])


def get_response_multiple(
    multiple: list[CashCollectionSchema],
) -> CashCollectionResponse:
    return CashCollectionResponse(cash_collections=multiple)


def _handle_history(
    db_session: Session,
    request: Request,
    cash_collection_id: int,
    request_object: CashCollectionRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryCashCollectionModel)
    if is_delete:
        history_service.delete_history_before_delete_object(
            request,
            HistoryCashCollectionModel.__tablename__,
            "cash_collection_id",
            cash_collection_id,
            "CashCollection",
            "HistoryCashCollection",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "cash_collection_id",
            cash_collection_id,
            "CashCollection",
            "HistoryCashCollection",
        )
