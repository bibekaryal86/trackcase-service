import sys
from http import HTTPStatus

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.service import schemas
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.ref_types import get_ref_types_service
from src.trackcase_service.utils.commons import (
    check_active_component_status,
    check_permissions,
    get_err_msg,
    get_read_response_data_metadata,
    raise_http_exception,
)
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)


class CourtCaseService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtCaseService, self).__init__(db_session, models.CourtCase)

    @check_permissions("COURT_CASES_CREATE")
    def create_court_case(
        self, request: Request, request_object: schemas.CourtCaseRequest
    ) -> schemas.CourtCaseResponse:
        try:
            data_model: models.CourtCase = convert_schema_to_model(
                request_object, models.CourtCase
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourtCase
            ).add_to_history(
                request,
                request_object,
                "court_case_id",
                data_model.id,
                "CourtCase",
                "HistoryCourtCase",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.CourtCase,
                exclusions=[
                    "filings",
                    "case_collections",
                    "hearing_calendars",
                    "history_court_cases",
                    "history_hearing_calendars",
                    "history_filings",
                    "history_case_collections",
                ],
            )
            return schemas.CourtCaseResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting CourtCase. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("COURT_CASES_READ")
    def read_court_case(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.CourtCaseResponse:
        try:
            if request_metadata:
                if request_metadata.schema_model_id:
                    read_response = self.read(
                        model_id=request_metadata.schema_model_id,
                        is_include_soft_deleted=request_metadata.is_include_deleted,
                    )
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
                    if not response_data:
                        raise_http_exception(
                            request,
                            HTTPStatus.NOT_FOUND,
                            f"CourtCase Not Found By Id: {request_metadata.schema_model_id}!!!",  # noqa: E501
                        )
                else:
                    read_response = self.read(
                        sort_config=request_metadata.sort_config,
                        filter_config=request_metadata.filter_config,
                        page_number=request_metadata.page_number,
                        per_page=request_metadata.per_page,
                        is_include_soft_deleted=request_metadata.is_include_deleted
                        is True,
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
                    schema_class=schemas.CourtCase,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "filings",
                        "case_collections",
                        "hearing_calendars",
                        "history_court_cases",
                        "history_hearing_calendars",
                        "history_filings",
                        "history_case_collections",
                    ],
                    extra_to_include=[
                        "filings",
                        "case_collections",
                        "hearing_calendars",
                    ],
                    history_to_include=["history_court_cases"],
                )
                for data_model in response_data
            ]
            return schemas.CourtCaseResponse(
                data=schema_models, metadata=response_metadata
            )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving CourtCase. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("COURT_CASES_UPDATE")
    def update_court_case(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.CourtCaseRequest,
        is_restore: bool = False,
    ) -> schemas.CourtCaseResponse:
        court_case_old = self.check_court_case_exists(model_id, request, is_restore)
        self.check_court_case_dependents_statuses(
            request, request_object.component_status_id, court_case_old
        )

        try:
            data_model: models.CourtCase = convert_schema_to_model(
                request_object, models.CourtCase
            )
            data_model = self.update(model_id, data_model, is_restore)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourtCase
            ).add_to_history(
                request,
                request_object,
                "court_case_id",
                data_model.id,
                "CourtCase",
                "HistoryCourtCase",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.CourtCase,
                exclusions=[
                    "filings",
                    "case_collections",
                    "hearing_calendars",
                    "history_court_cases",
                    "history_hearing_calendars",
                    "history_filings",
                    "history_case_collections",
                ],
            )
            return schemas.CourtCaseResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating CourtCase By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("COURT_CASES_DELETE")
    def delete_court_case(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CourtCaseResponse:
        court_case_old = self.check_court_case_exists(model_id, request, is_hard_delete)
        if court_case_old.filings:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete CourtCase {model_id}, There are Linked Filings!",  # noqa: E501
            )
        if court_case_old.case_collections:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete CourtCase {model_id}, There are Linked Case Collections!",  # noqa: E501
            )
        if court_case_old.hearing_calendars:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete CourtCase {model_id}, There are Linked Hearing Calendars!",  # noqa: E501
            )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourtCase
            ).delete_history_before_delete_object(
                models.HistoryCourtCase.__tablename__,
                "court_case_id",
                model_id,
                "CourtCase",
                "HistoryCourtCase",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourtCase
            ).add_to_history(
                request,
                court_case_old,
                "court_case_id",
                model_id,
                "CourtCase",
                "HistoryCourtCase",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CourtCaseResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting CourtCase By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_court_case_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ) -> schemas.CourtCase:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id,
            is_include_extra=True,
            is_include_deleted=is_include_deleted,
        )
        court_case_response = self.read_court_case(request, request_metadata)
        if not court_case_response or not court_case_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"CourtCase Not Found By Id: {model_id}!!!",
            )
        return court_case_response.data[0]

    def check_court_case_dependents_statuses(
        self,
        request: Request,
        status_new: int,
        court_case_old: schemas.CourtCase,
    ):
        status_old = court_case_old.component_status_id
        ref_types_service = get_ref_types_service(
            service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
            db_session=self.db_session,
        )
        court_case_active_statuses = ref_types_service.get_component_status(
            request,
            schemas.ComponentStatusNames.COURT_CASE,
            schemas.ComponentStatusTypes.ACTIVE,
        )
        active_status_ids_court_case = [
            component_status.id for component_status in court_case_active_statuses
        ]

        if status_new != status_old and status_new not in active_status_ids_court_case:
            if court_case_old.filings:
                filing_active_statuses = ref_types_service.get_component_status(
                    request,
                    schemas.ComponentStatusNames.FILING,
                    schemas.ComponentStatusTypes.ACTIVE,
                )
                active_status_ids_filing = [
                    component_status.id for component_status in filing_active_statuses
                ]
                if check_active_component_status(
                    court_case_old.filings, active_status_ids_filing
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update CourtCase {court_case_old.id} Status to {status_new}, There are Active Filings!",  # noqa: E501
                    )

            if court_case_old.case_collections:
                collection_active_statuses = ref_types_service.get_component_status(
                    request,
                    schemas.ComponentStatusNames.COLLECTION,
                    schemas.ComponentStatusTypes.ACTIVE,
                )
                active_status_ids_collection = [
                    component_status.id
                    for component_status in collection_active_statuses
                ]
                if check_active_component_status(
                    court_case_old.case_collections, active_status_ids_collection
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update CourtCase {court_case_old.id} Status to {status_new}, There are Active Case Collections!",  # noqa: E501
                    )

            if court_case_old.hearing_calendars:
                calendar_active_statuses = ref_types_service.get_component_status(
                    request,
                    schemas.ComponentStatusNames.CALENDAR,
                    schemas.ComponentStatusTypes.ACTIVE,
                )
                active_status_ids_calendar = [
                    component_status.id for component_status in calendar_active_statuses
                ]
                if check_active_component_status(
                    court_case_old.hearing_calendars, active_status_ids_calendar
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update CourtCase {court_case_old.id} Status to {status_new}, There are Active Hearing Calendars!",  # noqa: E501
                    )


def get_court_case_service(db_session: Session) -> CourtCaseService:
    return CourtCaseService(db_session)
