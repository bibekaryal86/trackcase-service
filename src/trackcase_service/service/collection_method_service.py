from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CollectionMethod as CollectionMethodModel
from src.trackcase_service.service.schemas import (
    CollectionMethod as CollectionMethodSchema,
)
from src.trackcase_service.service.schemas import (
    CollectionMethodRequest,
    CollectionMethodResponse,
)
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_collection_method_model_to_schema,
    convert_request_schema_to_model,
)


class CollectionMethodService(CrudService):
    def __init__(self, db_session: Session):
        super(CollectionMethodService, self).__init__(db_session, CollectionMethodModel)

    def create_one_collection_method(
        self, request: Request, request_object: CollectionMethodRequest
    ) -> CollectionMethodResponse:
        try:
            data_model: CollectionMethodModel = convert_request_schema_to_model(
                request_object, CollectionMethodModel
            )
            data_model = super().create(data_model)
            schema_model = convert_collection_method_model_to_schema(data_model)
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
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> CollectionMethodResponse:
        try:
            data_model: CollectionMethodModel = super().read_one(model_id)
            if data_model:
                schema_model: CollectionMethodSchema = (
                    convert_collection_method_model_to_schema(
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
                    f"Error Retrieving CollectionMethod By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )

    def read_all_collection_methods(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> CollectionMethodResponse:
        try:
            data_models: List[CollectionMethodModel] = super().read_all(
                sort_direction="asc", sort_by="name"
            )
            schema_models: List[CollectionMethodSchema] = [
                convert_collection_method_model_to_schema(
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
                    "Error Retrieving CollectionMethods. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_collection_method(
        self, model_id: int, request: Request, request_object: CollectionMethodRequest
    ) -> CollectionMethodResponse:
        collection_method_response = self.read_one_collection_method(model_id, request)

        if not (
            collection_method_response and collection_method_response.collection_methods
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CollectionMethod Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CollectionMethodModel = convert_request_schema_to_model(
                request_object, CollectionMethodModel
            )
            data_model = super().update(model_id, data_model)
            schema_model = convert_collection_method_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating CollectionMethod By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
            )

    def delete_one_collection_method(
        self, model_id: int, request: Request
    ) -> CollectionMethodResponse:
        collection_method_response = self.read_one_collection_method(model_id, request)

        if not (
            collection_method_response and collection_method_response.collection_methods
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CollectionMethod Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CollectionMethodResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting CollectionMethod By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
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
