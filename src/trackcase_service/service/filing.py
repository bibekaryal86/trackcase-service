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
    get_err_msg,
    get_read_response_data_metadata,
    raise_http_exception,
)
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)


class FilingService(CrudService):
    def __init__(self, db_session: Session):
        super(FilingService, self).__init__(db_session, models.Filing)

    def create_filing(
        self, request: Request, request_object: schemas.FilingRequest
    ) -> schemas.FilingResponse:
        try:
            data_model: models.Filing = convert_schema_to_model(
                request_object, models.Filing
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryFiling
            ).add_to_history(
                request,
                request_object,
                "filing_id",
                data_model.id,
                "Filing",
                "HistoryFiling",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Filing,
                exclusions=[
                    "task_calendars",
                    "history_filings",
                    "history_task_calendars",
                ],
            )
            return schemas.FilingResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting Filing. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_filing(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.FilingResponse:
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
                            f"Filing Not Found By Id: {request_metadata.model_id}!!!",
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
                    schema_class=schemas.Filing,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "task_calendars",
                        "history_filings",
                        "history_task_calendars",
                    ],
                    extra_to_include=["task_calendars"],
                    history_to_include=["history_filings"],
                )
                for data_model in response_data
            ]
            return schemas.FilingResponse(
                data=schema_models, metadata=response_metadata
            )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving Filing. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def update_filing(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.FilingRequest,
    ) -> schemas.FilingResponse:
        filing_old = self.check_filing_exists(model_id, request)
        self.check_filing_dependents_statuses(
            request, request_object.component_status_id, filing_old
        )

        try:
            data_model: models.Filing = convert_schema_to_model(
                request_object, models.Filing
            )
            data_model = self.update(model_id, data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryFiling
            ).add_to_history(
                request,
                request_object,
                "filing_id",
                data_model.id,
                "Filing",
                "HistoryFiling",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Filing,
                exclusions=[
                    "task_calendars",
                    "history_filings",
                    "history_task_calendars",
                ],
            )
            return schemas.FilingResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating Filing By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_filing(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.FilingResponse:
        filing_old = self.check_filing_exists(model_id, request)
        if filing_old.task_calendars:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete Filing {model_id}, There are Linked Task Calendars!",  # noqa: E501
            )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryFiling
            ).delete_history_before_delete_object(
                models.HistoryFiling.__tablename__,
                "filing_id",
                model_id,
                "Filing",
                "HistoryFiling",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryFiling
            ).add_to_history(
                request,
                filing_old,
                "filing_id",
                model_id,
                "Filing",
                "HistoryFiling",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.FilingResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Filing By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_filing_exists(self, model_id: int, request: Request) -> schemas.Filing:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_extra=True
        )
        filing_response = self.read_filing(request, request_metadata)
        if not filing_response or not filing_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Filing Not Found By Id: {model_id}!!!",
            )
        return filing_response.data[0]

    def check_filing_dependents_statuses(
        self,
        request: Request,
        status_new: int,
        filing_old: schemas.Filing,
    ):
        if filing_old.task_calendars:
            status_old = filing_old.component_status_id
            ref_types_service = get_ref_types_service(
                service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
                db_session=self.db_session,
            )
            filing_active_statuses = ref_types_service.get_component_status(
                request,
                schemas.ComponentStatusNames.FILING,
                schemas.ComponentStatusTypes.ACTIVE,
            )
            active_status_ids_filing = [
                component_status.id for component_status in filing_active_statuses
            ]
            if status_new != status_old and status_new not in active_status_ids_filing:
                calendar_active_statuses = ref_types_service.get_component_status(
                    request,
                    schemas.ComponentStatusNames.CALENDAR,
                    schemas.ComponentStatusTypes.ACTIVE,
                )
                active_status_ids_calendar = [
                    component_status.id for component_status in calendar_active_statuses
                ]

                if check_active_component_status(
                    filing_old.task_calendars, active_status_ids_calendar
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update Filing {filing_old.id} Status to {status_new}, There are Active Task Calendars!",  # noqa: E501
                    )


def get_filing_service(db_session: Session) -> FilingService:
    return FilingService(db_session)