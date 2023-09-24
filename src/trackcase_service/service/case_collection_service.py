from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import CaseCollection as CaseCollectionModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import CaseCollection as CaseCollectionSchema
from .schemas import CaseCollectionRequest, CaseCollectionResponse


class CaseCollectionService(CrudService):
    def __init__(self, db_session: Session):
        super(CaseCollectionService, self).__init__(db_session, CaseCollectionModel)

    def create_one_case_collection(
        self, request: Request, request_object: CaseCollectionRequest
    ) -> CaseCollectionResponse:
        try:
            data_model: CaseCollectionModel = copy_objects(
                request_object, CaseCollectionModel
            )
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting CaseCollection. Please Try Again!!!",
                str(ex),
            )

    def read_one_case_collection(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> CaseCollectionResponse:
        try:
            data_model: CaseCollectionModel = super().read_one(model_id)
            if data_model:
                schema_model: CaseCollectionSchema = _convert_model_to_schema(
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

    def read_all_case_collections(
        self, request: Request, is_include_extras: bool
    ) -> CaseCollectionResponse:
        try:
            data_models: List[CaseCollectionModel] = super().read_all()
            schema_models: List[CaseCollectionSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving CaseCollections. Please Try Again!!!",
                str(ex),
            )

    def update_one_case_collection(
        self, model_id: int, request: Request, request_object: CaseCollectionRequest
    ) -> CaseCollectionResponse:
        case_collection_response = self.read_one_case_collection(
            model_id, request, False
        )

        if not (case_collection_response and case_collection_response.case_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: CaseCollectionModel = copy_objects(
                request_object, CaseCollectionModel
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

    def delete_one_case_collection(
        self, model_id: int, request: Request
    ) -> CaseCollectionResponse:
        case_collection_response = self.read_one_case_collection(
            model_id, request, False
        )

        if not (case_collection_response and case_collection_response.case_collections):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return CaseCollectionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_case_collection_service(db_session: Session) -> CaseCollectionService:
    return CaseCollectionService(db_session)


def get_response_single(single: CaseCollectionSchema) -> CaseCollectionResponse:
    return CaseCollectionResponse(case_collections=[single])


def get_response_multiple(
    multiple: list[CaseCollectionSchema],
) -> CaseCollectionResponse:
    return CaseCollectionResponse(case_collections=multiple)


def _convert_model_to_schema(
    data_model: CaseCollectionModel, is_include_extras: bool = False
) -> CaseCollectionSchema:
    data_schema = CaseCollectionSchema(
        quote_date=data_model.quote_date,
        quote_amount=data_model.quote_amount,
        initial_payment=data_model.initial_payment,
        collection_method_id=data_model.collection_method_id,
        court_case_id=data_model.court_case_id,
        form_id=data_model.form_id
    )
    if is_include_extras:
        data_schema.collection_method = data_model.collection_method
        data_schema.court_case = data_model.court_case
        data_schema.form = data_model.form
    return data_schema
