import logging
import sys
from http import HTTPStatus
from typing import Type, Union

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.crud import CrudService, DataKeys
from src.trackcase_service.service import schemas
from src.trackcase_service.service.schemas import RefTypesServiceRegistry
from src.trackcase_service.utils import logger
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)

log = logger.Logger(logging.getLogger(__name__))


class ComponentStatusService(CrudService):
    def __init__(self, db_session: Session):
        super(ComponentStatusService, self).__init__(db_session, models.ComponentStatus)

    def create_component_status(
        self, request: Request, request_object: schemas.ComponentStatusRequest
    ) -> schemas.ComponentStatusResponse:
        try:
            data_model: models.ComponentStatus = convert_schema_to_model(
                request_object, models.ComponentStatus
            )
            data_model = self.create(data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model, schemas.ComponentStatus, []
            )

            return schemas.ComponentStatusResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting ComponentStatus. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_component_status(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.ComponentStatusResponse:
        try:
            if metadata is not None and metadata.request_object_id is not None:
                read_response = self.read(model_id=metadata.request_object_id)
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.request_object_id,
                    schemas.ComponentStatus,
                    schemas.ComponentStatusResponse,
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number or 1,
                    per_page=metadata.per_page or 100,
                    is_include_soft_deleted=metadata.is_include_deleted is True,
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
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving ComponentStatus. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_component_status_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        component_status_response = self.read_component_status(
            request, request_metadata
        )
        if not (component_status_response and component_status_response.data):
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
    ) -> schemas.ComponentStatusResponse:
        self.check_component_status_exists(model_id, request)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.ComponentStatus
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model, schemas.ComponentStatus, []
            )
            return schemas.ComponentStatusResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating ComponentStatus By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_component_status(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.ComponentStatusResponse:
        self.check_component_status_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.ComponentStatusResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
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
        try:
            data_model: models.CollectionMethod = convert_schema_to_model(
                request_object, models.CollectionMethod
            )
            data_model = self.create(data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.CollectionMethod,
                exclusions=["cash_collections", "history_cash_collections"],
            )

            return schemas.CollectionMethodResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting CollectionMethod. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_collection_method(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.CollectionMethodResponse:
        try:
            if metadata is not None and metadata.request_object_id is not None:
                read_response = self.read(model_id=metadata.request_object_id)
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.request_object_id,
                    schemas.CollectionMethod,
                    schemas.CollectionMethodResponse,
                    exclusions=["cash_collections", "history_cash_collections"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number or 1,
                    per_page=metadata.per_page or 100,
                    is_include_soft_deleted=metadata.is_include_deleted is True,
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
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving CollectionMethod. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_collection_method_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        collection_method_response = self.read_collection_method(
            request, request_metadata
        )
        if not (collection_method_response and collection_method_response.data):
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
    ) -> schemas.CollectionMethodResponse:
        self.check_collection_method_exists(model_id, request)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.CollectionMethod
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.CollectionMethod,
                exclusions=["cash_collections", "history_cash_collections"],
            )
            return schemas.CollectionMethodResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating CollectionMethod By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_collection_method(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CollectionMethodResponse:
        self.check_collection_method_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CollectionMethodResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
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
        try:
            data_model: models.CaseType = convert_schema_to_model(
                request_object, models.CaseType
            )
            data_model = self.create(data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.CaseType,
                exclusions=["court_cases", "history_court_cases"],
            )

            return schemas.CaseTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting CaseType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_case_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.CaseTypeResponse:
        try:
            if metadata is not None and metadata.request_object_id is not None:
                read_response = self.read(model_id=metadata.request_object_id)
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.request_object_id,
                    schemas.CaseType,
                    schemas.CaseTypeResponse,
                    exclusions=["court_cases", "history_court_cases"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number or 1,
                    per_page=metadata.per_page or 100,
                    is_include_soft_deleted=metadata.is_include_deleted is True,
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
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving CaseType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def check_case_type_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        case_type_response = self.read_case_type(request, request_metadata)
        if not (case_type_response and case_type_response.data):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CaseType Not Found By Id: {model_id}!!!",
            )

    def update_case_type(
        self, model_id: int, request: Request, request_object: schemas.CaseTypeRequest
    ) -> schemas.CaseTypeResponse:
        self.check_case_type_exists(model_id, request)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.CaseType
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.CaseType,
                exclusions=["court_cases", "history_court_cases"],
            )
            return schemas.CaseTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating CaseType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_case_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CaseTypeResponse:
        self.check_case_type_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CaseTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
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
        try:
            data_model: models.FilingType = convert_schema_to_model(
                request_object, models.FilingType
            )
            data_model = self.create(data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.FilingType,
                exclusions=["filings", "history_filings"],
            )

            return schemas.FilingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting FilingType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_filing_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.FilingTypeResponse:
        try:
            if metadata is not None and metadata.request_object_id is not None:
                read_response = self.read(model_id=metadata.request_object_id)
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.request_object_id,
                    schemas.FilingType,
                    schemas.FilingTypeResponse,
                    exclusions=["filings", "history_filings"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number or 1,
                    per_page=metadata.per_page or 100,
                    is_include_soft_deleted=metadata.is_include_deleted is True,
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
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving FilingType. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_filing_type_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        filing_type_response = self.read_filing_type(request, request_metadata)
        if not (filing_type_response and filing_type_response.data):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"FilingType Not Found By Id: {model_id}!!!",
            )

    def update_filing_type(
        self, model_id: int, request: Request, request_object: schemas.FilingTypeRequest
    ) -> schemas.FilingTypeResponse:
        self.check_filing_type_exists(model_id, request)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.FilingType
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.FilingType,
                exclusions=["filings", "history_filings"],
            )
            return schemas.FilingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating FilingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_filing_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.FilingTypeResponse:
        self.check_filing_type_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.FilingTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
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
        try:
            data_model: models.HearingType = convert_schema_to_model(
                request_object, models.HearingType
            )
            data_model = self.create(data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.HearingType,
                exclusions=["hearing_calendars", "history_hearing_calendars"],
            )

            return schemas.HearingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting HearingType. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_hearing_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.HearingTypeResponse:
        try:
            if metadata is not None and metadata.request_object_id is not None:
                read_response = self.read(model_id=metadata.request_object_id)
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.request_object_id,
                    schemas.HearingType,
                    schemas.HearingTypeResponse,
                    exclusions=["hearing_calendars", "history_hearing_calendars"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number or 1,
                    per_page=metadata.per_page or 100,
                    is_include_soft_deleted=metadata.is_include_deleted is True,
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
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving HearingType. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_hearing_type_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        hearing_type_response = self.read_hearing_type(request, request_metadata)
        if not (hearing_type_response and hearing_type_response.data):
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
    ) -> schemas.HearingTypeResponse:
        self.check_hearing_type_exists(model_id, request)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.HearingType
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.HearingType,
                exclusions=["hearing_calendars", "history_hearing_calendars"],
            )
            return schemas.HearingTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating HearingType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_hearing_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.HearingTypeResponse:
        self.check_hearing_type_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.HearingTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
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
        try:
            data_model: models.TaskType = convert_schema_to_model(
                request_object, models.TaskType
            )
            data_model = self.create(data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.TaskType,
                exclusions=["task_calendars", "history_task_calendars"],
            )

            return schemas.TaskTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting TaskType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_task_type(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.TaskTypeResponse:
        try:
            if metadata is not None and metadata.request_object_id is not None:
                read_response = self.read(model_id=metadata.request_object_id)
                return get_ref_types_response(
                    read_response,
                    True,
                    request,
                    metadata.request_object_id,
                    schemas.TaskType,
                    schemas.TaskTypeResponse,
                    exclusions=["task_calendars", "history_task_calendars"],
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number or 1,
                    per_page=metadata.per_page or 100,
                    is_include_soft_deleted=metadata.is_include_deleted is True,
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
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving TaskType. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def check_task_type_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        task_type_response = self.read_task_type(request, request_metadata)
        if not (task_type_response and task_type_response.data):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"TaskType Not Found By Id: {model_id}!!!",
            )

    def update_task_type(
        self, model_id: int, request: Request, request_object: schemas.TaskTypeRequest
    ) -> schemas.TaskTypeResponse:
        self.check_task_type_exists(model_id, request)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.TaskType
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_ref_types_model_to_schema(
                data_model,
                schemas.TaskType,
                exclusions=["task_calendars", "history_task_calendars"],
            )
            return schemas.TaskTypeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating TaskType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_task_type(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.TaskTypeResponse:
        self.check_task_type_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.TaskTypeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting TaskType By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


def get_ref_types_service(
    service_type: RefTypesServiceRegistry, db_session: Session
) -> (
    ComponentStatusService
    | CollectionMethodService
    | CaseTypeService
    | FilingTypeService
    | HearingTypeService
    | TaskTypeService
):
    service_registry = {
        RefTypesServiceRegistry.COMPONENT_STATUS: ComponentStatusService,
        RefTypesServiceRegistry.COLLECTION_METHOD: CollectionMethodService,
        RefTypesServiceRegistry.CASE_TYPE: CaseTypeService,
        RefTypesServiceRegistry.FILING_TYPE: FilingTypeService,
        RefTypesServiceRegistry.HEARING_TYPE: HearingTypeService,
        RefTypesServiceRegistry.TASK_TYPE: TaskTypeService,
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
    if is_single:
        data_models = [data_models]

    metadata = read_response.get(DataKeys.metadata)
    schema_models = [
        convert_ref_types_model_to_schema(data_model, schema_type, exclusions)
        for data_model in data_models
    ]
    return return_type(
        **{
            "metadata": metadata,
            "data": schema_models,
        }
    )


def convert_ref_types_model_to_schema(
    data_model: Union[
        models.ComponentStatus,
        models.CollectionMethod,
        models.CaseType,
        models.FilingType,
        models.HearingType,
        models.TaskType,
    ],
    schema_class: Type[
        Union[
            schemas.ComponentStatus,
            schemas.CollectionMethod,
            schemas.CaseType,
            schemas.FilingType,
            schemas.HearingType,
            schemas.TaskType,
        ]
    ],
    exclusions: list[str],
) -> Union[
    schemas.ComponentStatus,
    schemas.CollectionMethod,
    schemas.CaseType,
    schemas.FilingType,
    schemas.HearingType,
    schemas.TaskType,
]:
    return convert_model_to_schema(
        data_model=data_model,
        schema_class=schema_class,
        exclusions=exclusions,
    )
