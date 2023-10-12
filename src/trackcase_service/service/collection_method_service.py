from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CollectionMethod as CollectionMethodModel
from src.trackcase_service.utils.commons import (
    copy_objects,
    get_err_msg,
    raise_http_exception,
)

from .schemas import CollectionMethod as CollectionMethodSchema
from .schemas import CollectionMethodRequest, CollectionMethodResponse


class CollectionMethodService(CrudService):
    def __init__(self, db_session: Session):
        super(CollectionMethodService, self).__init__(db_session, CollectionMethodModel)

    def create_one_collection_method(
        self, request: Request, request_object: CollectionMethodRequest
    ) -> CollectionMethodResponse:
        try:
            data_model: CollectionMethodModel = copy_objects(
                request_object, CollectionMethodModel
            )
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting CollectionMethod. Please Try Again!!!", str(ex)
                ),
            )

    def read_one_collection_method(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> CollectionMethodResponse:
        try:
            data_model: CollectionMethodModel = super().read_one(model_id)
            if data_model:
                schema_model: CollectionMethodSchema = _convert_model_to_schema(
                    data_model, is_include_extras
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )

    def read_all_collection_methods(
        self, request: Request, is_include_extras: bool
    ) -> CollectionMethodResponse:
        try:
            data_models: List[CollectionMethodModel] = super().read_all()
            schema_models: List[CollectionMethodSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving CollectionMethods. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_collection_method(
        self, model_id: int, request: Request, request_object: CollectionMethodRequest
    ) -> CollectionMethodResponse:
        collection_method_response = self.read_one_collection_method(
            model_id, request, False
        )

        if not (
            collection_method_response and collection_method_response.collection_methods
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CollectionMethodModel = copy_objects(
                request_object, CollectionMethodModel
            )
            data_model = super().update(model_id, data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )

    def delete_one_collection_method(
        self, model_id: int, request: Request
    ) -> CollectionMethodResponse:
        collection_method_response = self.read_one_collection_method(
            model_id, request, False
        )

        if not (
            collection_method_response and collection_method_response.collection_methods
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CollectionMethodResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )


def get_collection_method_service(db_session: Session) -> CollectionMethodService:
    return CollectionMethodService(db_session)


def get_response_single(single: CollectionMethodSchema) -> CollectionMethodResponse:
    return CollectionMethodResponse(collection_methods=[single])


def get_response_multiple(
    multiple: list[CollectionMethodSchema],
) -> CollectionMethodResponse:
    return CollectionMethodResponse(collection_methods=multiple)


def _convert_model_to_schema(
    data_model: CollectionMethodModel, is_include_extras: bool = False
) -> CollectionMethodSchema:
    data_schema = CollectionMethodSchema(
        id=data_model.id,
        created=data_model.created,
        modified=data_model.modified,
        name=data_model.name,
        description=data_model.description,
    )
    if is_include_extras:
        data_schema.cash_collections = data_model.cash_collections
        data_schema.case_collections = data_model.case_collections
    return data_schema
