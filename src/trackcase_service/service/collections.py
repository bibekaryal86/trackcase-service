import sys
from http import HTTPStatus
from http.client import HTTPException

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.service import schemas
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.ref_types import get_ref_types_service
from src.trackcase_service.utils.commons import (
    check_active_component_status,
    get_err_msg,
    get_read_response_data_metadata,
    raise_http_exception,
)
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)


class CaseCollectionService(CrudService):
    def __init__(self, db_session: Session):
        super(CaseCollectionService, self).__init__(db_session, models.CaseCollection)

    def create_case_collection(
        self, request: Request, request_object: schemas.CaseCollectionRequest
    ) -> schemas.CaseCollectionResponse:
        try:
            data_model: models.CaseCollection = convert_schema_to_model(
                request_object, models.CaseCollection
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCaseCollection
            ).add_to_history(
                request,
                request_object,
                "case_collection_id",
                data_model.id,
                "CaseCollection",
                "HistoryCaseCollection",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.CaseCollection,
                exclusions=[
                    "cash_collections",
                    "history_case_collections",
                    "history_cash_collections",
                ],
            )
            return schemas.CaseCollectionResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting Case Collection. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_case_collection(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.CaseCollectionResponse:
        try:
            if request_metadata:
                if request_metadata.model_id:
                    read_response = self.read(model_id=request_metadata.model_id)
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
                    if not response_data:
                        raise_http_exception(
                            request,
                            HTTPStatus.NOT_FOUND,
                            f"Case Collection Not Found By Id: {request_metadata.model_id}!!!",
                        )
                else:
                    read_response = self.read(
                        sort_config=request_metadata.sort_config,
                        filter_config=request_metadata.filter_config,
                        page_number=request_metadata.page_number,
                        per_page=request_metadata.per_page,
                        is_include_soft_deleted=request_metadata.is_include_deleted,
                    )
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
            else:
                request_metadata = schemas.RequestMetadata()
                read_response = self.read()
                response_data, response_metadata = get_read_response_data_metadata(
                    read_response
                )

            schema_models = [
                convert_model_to_schema(
                    data_model=data_model,
                    schema_class=schemas.CaseCollection,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "cash_collections",
                        "history_case_collections",
                        "history_cash_collections",
                    ],
                    extra_to_include=["cash_collections"],
                    history_to_include=["history_case_collections"],
                )
                for data_model in response_data
            ]
            return schemas.CaseCollectionResponse(
                data=schema_models, metadata=response_metadata
            )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving Case Collection. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def update_case_collection(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.CaseCollectionRequest,
    ) -> schemas.CaseCollectionResponse:
        case_collection_old = self.check_case_collection_exists(model_id, request)
        self.check_case_collection_dependents_statuses(
            request, request_object.component_status_id, case_collection_old
        )

        try:
            data_model: models.CaseCollection = convert_schema_to_model(
                request_object, models.CaseCollection
            )
            data_model = self.update(model_id, data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCaseCollection
            ).add_to_history(
                request,
                request_object,
                "case_collection_id",
                data_model.id,
                "CaseCollection",
                "HistoryCaseCollection",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.CaseCollection,
                exclusions=[
                    "cash_collections",
                    "history_case_collections",
                    "history_cash_collections",
                ],
            )
            return schemas.CaseCollectionResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating Case Collection By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_case_collection(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CaseCollectionResponse:
        case_collection_old = self.check_case_collection_exists(model_id, request)
        if case_collection_old.cash_collections:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete Case Collection {model_id}, There are Linked Cash Collections!",  # noqa: E501
            )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCaseCollection
            ).delete_history_before_delete_object(
                models.HistoryCaseCollection.__tablename__,
                "case_collection_id",
                model_id,
                "CaseCollection",
                "HistoryCaseCollection",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCaseCollection
            ).add_to_history(
                request,
                case_collection_old,
                "case_collection_id",
                model_id,
                "CaseCollection",
                "HistoryCaseCollection",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CaseCollectionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Case Collection By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_case_collection_exists(
        self, model_id: int, request: Request
    ) -> schemas.CaseCollection:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_extra=True
        )
        case_collection_response = self.read_case_collection(request, request_metadata)
        if not case_collection_response or not case_collection_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Case Collection Not Found By Id: {model_id}!!!",
            )
        return case_collection_response.data[0]

    def check_case_collection_dependents_statuses(
        self,
        request: Request,
        status_new: int,
        case_collection_old: schemas.CaseCollection,
    ):
        if case_collection_old.cash_collections:
            status_old = case_collection_old.component_status_id
            collection_active_statuses = get_ref_types_service(
                service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
                db_session=self.db_session,
            ).get_component_status(
                request,
                schemas.ComponentStatusNames.COLLECTION,
                schemas.ComponentStatusTypes.ACTIVE,
            )
            active_status_ids = [
                component_status.id
                for component_status in collection_active_statuses
            ]

            if status_new != status_old and status_new not in active_status_ids:
                if check_active_component_status(
                    case_collection_old.cash_collections, active_status_ids
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update Case Collection {case_collection_old.id} Status to {status_new}, There are Active Cash Collections!",  # noqa: E501
                    )


class CashCollectionService(CrudService):
    def __init__(self, db_session: Session):
        super(CashCollectionService, self).__init__(db_session, models.CashCollection)

    def create_cash_collection(
        self, request: Request, request_object: schemas.CashCollectionRequest
    ) -> schemas.CashCollectionResponse:
        try:
            data_model: models.CashCollection = convert_schema_to_model(
                request_object, models.CashCollection
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCashCollection
            ).add_to_history(
                request,
                request_object,
                "cash_collection_id",
                data_model.id,
                "CashCollection",
                "HistoryCashCollection",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.CashCollection,
                exclusions=[
                    "history_cash_collections",
                ],
            )
            return schemas.CashCollectionResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting Cash Collection. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_cash_collection(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.CashCollectionResponse:
        try:
            if request_metadata:
                if request_metadata.model_id:
                    read_response = self.read(model_id=request_metadata.model_id)
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
                    if not response_data:
                        raise_http_exception(
                            request,
                            HTTPStatus.NOT_FOUND,
                            f"Cash Collection Not Found By Id: {request_metadata.model_id}!!!",
                        )
                else:
                    read_response = self.read(
                        sort_config=request_metadata.sort_config,
                        filter_config=request_metadata.filter_config,
                        page_number=request_metadata.page_number,
                        per_page=request_metadata.per_page,
                        is_include_soft_deleted=request_metadata.is_include_deleted,
                    )
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
            else:
                request_metadata = schemas.RequestMetadata()
                read_response = self.read()
                response_data, response_metadata = get_read_response_data_metadata(
                    read_response
                )

            schema_models = [
                convert_model_to_schema(
                    data_model=data_model,
                    schema_class=schemas.CashCollection,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "history_cash_collections",
                    ],
                    history_to_include=["history_cash_collections"],
                )
                for data_model in response_data
            ]
            return schemas.CashCollectionResponse(
                data=schema_models, metadata=response_metadata
            )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving Cash Collection. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def update_cash_collection(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.CashCollectionRequest,
    ) -> schemas.CashCollectionResponse:
        self.check_cash_collection_exists(model_id, request)

        try:
            data_model: models.CashCollection = convert_schema_to_model(
                request_object, models.CashCollection
            )
            data_model = self.update(model_id, data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCashCollection
            ).add_to_history(
                request,
                request_object,
                "cash_collection_id",
                data_model.id,
                "CashCollection",
                "HistoryCashCollection",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.CashCollection,
                exclusions=[
                    "history_cash_collections",
                ],
            )
            return schemas.CashCollectionResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating Cash Collection By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_cash_collection(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CashCollectionResponse:
        cash_collection_old = self.check_cash_collection_exists(model_id, request)

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCashCollection
            ).delete_history_before_delete_object(
                models.HistoryCashCollection.__tablename__,
                "cash_collection_id",
                model_id,
                "CashCollection",
                "HistoryCashCollection",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCashCollection
            ).add_to_history(
                request,
                cash_collection_old,
                "cash_collection_id",
                model_id,
                "CashCollection",
                "HistoryCashCollection",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CashCollectionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Cash Collection By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_cash_collection_exists(
        self, model_id: int, request: Request
    ) -> schemas.CashCollection:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_extra=True
        )
        cash_collection_response = self.read_cash_collection(request, request_metadata)
        if not cash_collection_response or not cash_collection_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Cash Collection Not Found By Id: {model_id}!!!",
            )
        return cash_collection_response.data[0]


def get_collection_service(
    service_type: schemas.CollectionServiceRegistry, db_session: Session
) -> CaseCollectionService | CashCollectionService:
    service_registry = {
        schemas.CollectionServiceRegistry.CASE_COLLECTION: CaseCollectionService,
        schemas.CollectionServiceRegistry.CASH_COLLECTION: CashCollectionService,
    }
    return service_registry.get(service_type)(db_session)
