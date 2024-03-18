import logging
import sys
from http import HTTPStatus
from typing import Type, Union

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.crud import CrudService, DataKeys
from src.trackcase_service.service import schemas
from src.trackcase_service.utils.cache import get_ref_types_cache, set_ref_types_cache
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)
from src.trackcase_service.utils.logger import Logger

log = Logger(logging.getLogger(__name__))


class ComponentStatusService(CrudService):
    def __init__(self, db_session: Session):
        super(ComponentStatusService, self).__init__(db_session, models.ComponentStatus)

    def create_component_status(
        self, request: Request, request_object: schemas.ComponentStatusRequest
    ) -> schemas.ComponentStatusResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.COMPONENT_STATUS, [])

        try:
            data_model: models.ComponentStatus = convert_schema_to_model(
                request_object, models.ComponentStatus
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.ComponentStatus,
            )
            return schemas.ComponentStatusResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting ComponentStatus. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_component_status(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.ComponentStatusResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(
                    model_id=metadata.model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.ComponentStatus,
                    schemas.ComponentStatusResponse,
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.ComponentStatus,
                    return_type=schemas.ComponentStatusResponse,
                )
            else:
                read_response = self.read()
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.ComponentStatus,
                    return_type=schemas.ComponentStatusResponse,
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving ComponentStatus. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def get_component_status(
        self,
        request: Request,
        component_name: schemas.ComponentStatusNames,
        status_type: schemas.ComponentStatusTypes = None,
    ) -> list[schemas.ComponentStatus]:
        component_statuses = get_ref_types_cache(
            schemas.RefTypesServiceRegistry.COMPONENT_STATUS
        )
        if not component_statuses:
            component_statuses = self.read_component_status(request).data or []
            set_ref_types_cache(
                schemas.RefTypesServiceRegistry.COMPONENT_STATUS, component_statuses
            )
        component_name_statuses = [
            component_status
            for component_status in component_statuses
            if component_status.component_name == component_name
        ]
        if not status_type or status_type == schemas.ComponentStatusTypes.ALL:
            return component_name_statuses
        elif status_type == schemas.ComponentStatusTypes.ACTIVE:
            return [
                component_status
                for component_status in component_name_statuses
                if component_status.is_active is True
            ]
        else:
            return [
                component_status
                for component_status in component_name_statuses
                if component_status.is_active is False
            ]
        # return list(
        #     filter(
        #         lambda component_status: component_status.component_name
        #         == component_name,
        #         component_statuses,
        #     )
        # )

    def check_component_status_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        component_status_response = self.read_component_status(
            request, request_metadata
        )
        if not component_status_response or not component_status_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"ComponentStatus Not Found By Id: {model_id}!!!",
            )

    def update_component_status(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.ComponentStatusRequest,
        is_restore: bool = False,
    ) -> schemas.ComponentStatusResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.COMPONENT_STATUS, [])
        self.check_component_status_exists(model_id, request, is_restore)

        try:
            data_model: models.ComponentStatus = convert_schema_to_model(
                request_object, models.ComponentStatus
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.ComponentStatus,
            )
            return schemas.ComponentStatusResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating ComponentStatus By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_component_status(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.ComponentStatusResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.COMPONENT_STATUS, [])
        self.check_component_status_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.ComponentStatusResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting ComponentStatus By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class CollectionMethodService(CrudService):
    def __init__(self, db_session: Session):
        super(CollectionMethodService, self).__init__(
            db_session, models.CollectionMethod
        )

    def create_collection_method(
        self, request: Request, request_object: schemas.CollectionMethodRequest
    ) -> schemas.CollectionMethodResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.COLLECTION_METHOD, [])
        try:
            data_model: models.CollectionMethod = convert_schema_to_model(
                request_object, models.CollectionMethod
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.CollectionMethod,
                exclusions=["cash_collections", "history_cash_collections"],
            )
            return schemas.CollectionMethodResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting CollectionMethod. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_collection_method(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.CollectionMethodResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(
                    model_id=metadata.model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.CollectionMethod,
                    schemas.CollectionMethodResponse,
                    exclusions=["cash_collections", "history_cash_collections"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.CollectionMethod,
                    return_type=schemas.CollectionMethodResponse,
                    exclusions=["cash_collections", "history_cash_collections"],
                )
            else:
                read_response = self.read()
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.CollectionMethod,
                    return_type=schemas.CollectionMethodResponse,
                    exclusions=["cash_collections", "history_cash_collections"],
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving CollectionMethod. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def get_collection_method(
        self,
        request: Request,
    ) -> list[schemas.CollectionMethod]:
        collection_methods = get_ref_types_cache(
            schemas.RefTypesServiceRegistry.COLLECTION_METHOD
        )
        if not collection_methods:
            collection_methods = self.read_collection_method(request).data or []
            set_ref_types_cache(
                schemas.RefTypesServiceRegistry.COLLECTION_METHOD, collection_methods
            )
            return collection_methods

    def check_collection_method_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        collection_method_response = self.read_collection_method(
            request, request_metadata
        )
        if not collection_method_response or not collection_method_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CollectionMethod Not Found By Id: {model_id}!!!",
            )

    def update_collection_method(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.CollectionMethodRequest,
        is_restore: bool = False,
    ) -> schemas.CollectionMethodResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.COLLECTION_METHOD, [])
        self.check_collection_method_exists(model_id, request, is_restore)

        try:
            data_model: models.CollectionMethod = convert_schema_to_model(
                request_object, models.CollectionMethod
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.CollectionMethod,
                exclusions=["cash_collections", "history_cash_collections"],
            )
            return schemas.CollectionMethodResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating CollectionMethod By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_collection_method(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CollectionMethodResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.COLLECTION_METHOD, [])
        self.check_collection_method_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CollectionMethodResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting CollectionMethod By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class CaseTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(CaseTypeService, self).__init__(db_session, models.CaseType)

    def create_case_type(
        self, request: Request, request_object: schemas.CaseTypeRequest
    ) -> schemas.CaseTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.CASE_TYPE, [])
        try:
            data_model: models.CaseType = convert_schema_to_model(
                request_object, models.CaseType
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.CaseType,
                exclusions=["court_cases", "history_court_cases"],
            )
            return schemas.CaseTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting CaseType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_case_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.CaseTypeResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(
                    model_id=metadata.model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.CaseType,
                    schemas.CaseTypeResponse,
                    exclusions=["court_cases", "history_court_cases"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.CaseType,
                    return_type=schemas.CaseTypeResponse,
                    exclusions=["court_cases", "history_court_cases"],
                )
            else:
                read_response = self.read()
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.CaseType,
                    return_type=schemas.CaseTypeResponse,
                    exclusions=["court_cases", "history_court_cases"],
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving CaseType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def get_case_type(
        self,
        request: Request,
    ) -> list[schemas.CaseType]:
        case_types = get_ref_types_cache(schemas.RefTypesServiceRegistry.CASE_TYPE)
        if not case_types:
            case_types = self.read_case_type(request).data or []
            set_ref_types_cache(schemas.RefTypesServiceRegistry.CASE_TYPE, case_types)
            return case_types

    def check_case_type_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        case_type_response = self.read_case_type(request, request_metadata)
        if not case_type_response or not case_type_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CaseType Not Found By Id: {model_id}!!!",
            )

    def update_case_type(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.CaseTypeRequest,
        is_restore: bool = False,
    ) -> schemas.CaseTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.CASE_TYPE, [])
        self.check_case_type_exists(model_id, request, is_restore)

        try:
            data_model: models.CaseType = convert_schema_to_model(
                request_object, models.CaseType
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.CaseType,
                exclusions=["court_cases", "history_court_cases"],
            )
            return schemas.CaseTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating CaseType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_case_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CaseTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.CASE_TYPE, [])
        self.check_case_type_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CaseTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting CaseType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class FilingTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(FilingTypeService, self).__init__(db_session, models.FilingType)

    def create_filing_type(
        self, request: Request, request_object: schemas.FilingTypeRequest
    ) -> schemas.FilingTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.FILING_TYPE, [])
        try:
            data_model: models.FilingType = convert_schema_to_model(
                request_object, models.FilingType
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.FilingType,
                exclusions=["filings", "history_filings"],
            )
            return schemas.FilingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting FilingType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_filing_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.FilingTypeResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(
                    model_id=metadata.model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.FilingType,
                    schemas.FilingTypeResponse,
                    exclusions=["filings", "history_filings"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.FilingType,
                    return_type=schemas.FilingTypeResponse,
                    exclusions=["filings", "history_filings"],
                )
            else:
                read_response = self.read()
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.FilingType,
                    return_type=schemas.FilingTypeResponse,
                    exclusions=["filings", "history_filings"],
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving FilingType. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def get_filing_type(
        self,
        request: Request,
    ) -> list[schemas.FilingType]:
        filing_types = get_ref_types_cache(schemas.RefTypesServiceRegistry.FILING_TYPE)
        if not filing_types:
            filing_types = self.read_filing_type(request).data or []
            set_ref_types_cache(
                schemas.RefTypesServiceRegistry.FILING_TYPE, filing_types
            )
            return filing_types

    def check_filing_type_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        filing_type_response = self.read_filing_type(request, request_metadata)
        if not filing_type_response or not filing_type_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"FilingType Not Found By Id: {model_id}!!!",
            )

    def update_filing_type(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.FilingTypeRequest,
        is_restore: bool = False,
    ) -> schemas.FilingTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.FILING_TYPE, [])
        self.check_filing_type_exists(model_id, request, is_restore)

        try:
            data_model: models.FilingType = convert_schema_to_model(
                request_object, models.FilingType
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.FilingType,
                exclusions=["filings", "history_filings"],
            )
            return schemas.FilingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating FilingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_filing_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.FilingTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.FILING_TYPE, [])
        self.check_filing_type_exists(model_id, request, is_hard_delete)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.FilingTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting FilingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class HearingTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(HearingTypeService, self).__init__(db_session, models.HearingType)

    def create_hearing_type(
        self, request: Request, request_object: schemas.HearingTypeRequest
    ) -> schemas.HearingTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.HEARING_TYPE, [])
        try:
            data_model: models.HearingType = convert_schema_to_model(
                request_object, models.HearingType
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.HearingType,
                exclusions=["hearing_calendars", "history_hearing_calendars"],
            )
            return schemas.HearingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting HearingType. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_hearing_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.HearingTypeResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(
                    model_id=metadata.model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.HearingType,
                    schemas.HearingTypeResponse,
                    exclusions=["hearing_calendars", "history_hearing_calendars"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.HearingType,
                    return_type=schemas.HearingTypeResponse,
                    exclusions=["hearing_calendars", "history_hearing_calendars"],
                )
            else:
                read_response = self.read()
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.HearingType,
                    return_type=schemas.HearingTypeResponse,
                    exclusions=["hearing_calendars", "history_hearing_calendars"],
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving HearingType. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def get_hearing_type(
        self,
        request: Request,
    ) -> list[schemas.HearingType]:
        hearing_types = get_ref_types_cache(
            schemas.RefTypesServiceRegistry.HEARING_TYPE
        )
        if not hearing_types:
            hearing_types = self.read_hearing_type(request).data or []
            set_ref_types_cache(
                schemas.RefTypesServiceRegistry.HEARING_TYPE, hearing_types
            )
            return hearing_types

    def check_hearing_type_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        hearing_type_response = self.read_hearing_type(request, request_metadata)
        if not hearing_type_response or not hearing_type_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"HearingType Not Found By Id: {model_id}!!!",
            )

    def update_hearing_type(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.HearingTypeRequest,
        is_restore: bool = False,
    ) -> schemas.HearingTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.HEARING_TYPE, [])
        self.check_hearing_type_exists(model_id, request, is_restore)

        try:
            data_model: models.HearingType = convert_schema_to_model(
                request_object, models.HearingType
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.HearingType,
                exclusions=["hearing_calendars", "history_hearing_calendars"],
            )
            return schemas.HearingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating HearingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_hearing_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.HearingTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.HEARING_TYPE, [])
        self.check_hearing_type_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.HearingTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting HearingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class TaskTypeService(CrudService):
    def __init__(self, db_session: Session):
        super(TaskTypeService, self).__init__(db_session, models.TaskType)

    def create_task_type(
        self, request: Request, request_object: schemas.TaskTypeRequest
    ) -> schemas.TaskTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.TASK_TYPE, [])
        try:
            data_model: models.TaskType = convert_schema_to_model(
                request_object, models.TaskType
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.TaskType,
                exclusions=["task_calendars", "history_task_calendars"],
            )
            return schemas.TaskTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting TaskType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_task_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.TaskTypeResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(
                    model_id=metadata.model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.TaskType,
                    schemas.TaskTypeResponse,
                    exclusions=["task_calendars", "history_task_calendars"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.TaskType,
                    return_type=schemas.TaskTypeResponse,
                    exclusions=["task_calendars", "history_task_calendars"],
                )
            else:
                read_response = self.read()
                return get_ref_types_response(
                    read_response,
                    schema_type=schemas.TaskType,
                    return_type=schemas.TaskTypeResponse,
                    exclusions=["task_calendars", "history_task_calendars"],
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving TaskType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def get_task_type(
        self,
        request: Request,
    ) -> list[schemas.TaskType]:
        task_types = get_ref_types_cache(schemas.RefTypesServiceRegistry.TASK_TYPE)
        if not task_types:
            task_types = self.read_task_type(request).data or []
            set_ref_types_cache(schemas.RefTypesServiceRegistry.TASK_TYPE, task_types)
            return task_types

    def check_task_type_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        task_type_response = self.read_task_type(request, request_metadata)
        if not task_type_response or not task_type_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"TaskType Not Found By Id: {model_id}!!!",
            )

    def update_task_type(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.TaskTypeRequest,
        is_restore: bool = False,
    ) -> schemas.TaskTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.TASK_TYPE, [])
        self.check_task_type_exists(model_id, request, is_restore)

        try:
            data_model: models.TaskType = convert_schema_to_model(
                request_object, models.TaskType
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.TaskType,
                exclusions=["task_calendars", "history_task_calendars"],
            )
            return schemas.TaskTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating TaskType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_task_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.TaskTypeResponse:
        set_ref_types_cache(schemas.RefTypesServiceRegistry.TASK_TYPE, [])
        self.check_task_type_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.TaskTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting TaskType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


def get_ref_types_service(
    service_type: schemas.RefTypesServiceRegistry, db_session: Session
) -> (
    ComponentStatusService
    | CollectionMethodService
    | CaseTypeService
    | FilingTypeService
    | HearingTypeService
    | TaskTypeService
):
    service_registry = {
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS: ComponentStatusService,
        schemas.RefTypesServiceRegistry.COLLECTION_METHOD: CollectionMethodService,
        schemas.RefTypesServiceRegistry.CASE_TYPE: CaseTypeService,
        schemas.RefTypesServiceRegistry.FILING_TYPE: FilingTypeService,
        schemas.RefTypesServiceRegistry.HEARING_TYPE: HearingTypeService,
        schemas.RefTypesServiceRegistry.TASK_TYPE: TaskTypeService,
    }
    return service_registry.get(service_type)(db_session)


def get_ref_types_response(
    read_response,
    is_single=False,
    request: Request = None,
    model_id: int = None,
    schema_type: Union[
        Type[schemas.ComponentStatus],
        Type[schemas.CollectionMethod],
        Type[schemas.CaseType],
        Type[schemas.FilingType],
        Type[schemas.HearingType],
        Type[schemas.TaskType],
    ] = None,
    return_type: Union[
        Type[schemas.ComponentStatusResponse],
        Type[schemas.CollectionMethodResponse],
        Type[schemas.CaseTypeResponse],
        Type[schemas.FilingTypeResponse],
        Type[schemas.HearingTypeResponse],
        Type[schemas.TaskTypeResponse],
    ] = None,
    exclusions=None,
) -> Union[
    schemas.ComponentStatusResponse,
    schemas.CollectionMethodResponse,
    schemas.CaseTypeResponse,
    schemas.FilingTypeResponse,
    schemas.HearingTypeResponse,
    schemas.TaskTypeResponse,
]:
    if exclusions is None:
        exclusions = []
    if is_single and not read_response.get(DataKeys.data):
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"{schema_type.__name__} Not Found By Id: {model_id}!!!",
        )
    data_models = read_response.get(DataKeys.data)
    metadata = read_response.get(DataKeys.metadata)
    schema_models = [
        convert_model_to_schema(
            data_model=data_model, schema_class=schema_type, exclusions=exclusions
        )
        for data_model in data_models
    ]
    return return_type(
        **{
            "metadata": metadata,
            "data": schema_models,
        }
    )
