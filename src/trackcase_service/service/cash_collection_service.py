from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CashCollection as CashCollectionModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import CashCollection as CashCollectionSchema
from .schemas import CashCollectionRequest, CashCollectionResponse


class CashCollectionService(CrudService):
    def __init__(self, db_session: Session):
        super(CashCollectionService, self).__init__(db_session, CashCollectionModel)

    def create_one_cash_collection(
        self, request: Request, request_object: CashCollectionRequest
    ) -> CashCollectionResponse:
        try:
            data_model: CashCollectionModel = copy_objects(
                request_object, CashCollectionModel
            )
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting CashCollection. Please Try Again!!!",
                str(ex),
            )

    def read_one_cash_collection(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> CashCollectionResponse:
        try:
            data_model: CashCollectionModel = super().read_one(model_id)
            if data_model:
                schema_model: CashCollectionSchema = _convert_model_to_schema(
                    data_model, is_include_extras
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def read_all_cash_collections(
        self, request: Request, is_include_extras: bool
    ) -> CashCollectionResponse:
        try:
            data_models: List[CashCollectionModel] = super().read_all()
            schema_models: List[CashCollectionSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving CashCollections. Please Try Again!!!",
                str(ex),
            )

    def update_one_cash_collection(
        self, model_id: int, request: Request, request_object: CashCollectionRequest
    ) -> CashCollectionResponse:
        cash_collection_response = self.read_one_cash_collection(
            model_id, request, False
        )

        if not (cash_collection_response and cash_collection_response.cash_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CashCollectionModel = copy_objects(
                request_object, CashCollectionModel
            )
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

    def delete_one_cash_collection(
        self, model_id: int, request: Request
    ) -> CashCollectionResponse:
        cash_collection_response = self.read_one_cash_collection(
            model_id, request, False
        )

        if not (cash_collection_response and cash_collection_response.cash_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CashCollectionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_cash_collection_service(db_session: Session) -> CashCollectionService:
    return CashCollectionService(db_session)


def get_response_single(single: CashCollectionSchema) -> CashCollectionResponse:
    return CashCollectionResponse(cash_collections=[single])


def get_response_multiple(
    multiple: list[CashCollectionSchema],
) -> CashCollectionResponse:
    return CashCollectionResponse(cash_collections=multiple)


def _convert_model_to_schema(
    data_model: CashCollectionModel, is_include_extras: bool = False
) -> CashCollectionSchema:
    data_schema = CashCollectionSchema(
        collection_date=data_model.collection_date,
        collected_amount=data_model.collected_amount,
        waived_amount=data_model.waived_amount,
        memo=data_model.memo,
        collection_method_id=data_model.collection_method_id,
        case_collection_id=data_model.case_collection_id,
    )
    if is_include_extras:
        data_schema.collection_method = data_model.collection_method
        data_schema.case_collection = data_model.case_collection
    return data_schema
