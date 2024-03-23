import sys
from datetime import datetime, timedelta
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
    check_permissions,
    get_err_msg,
    get_read_response_data_metadata,
    raise_http_exception,
)
from src.trackcase_service.utils.constants import (
    DEFAULT_HEARING_TO_TASK_CALENDAR_DATE,
    HEARING_TO_TASK_CALENDAR_DATE,
    TASK_ID_DUE_AT_HEARING,
)
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)


class HearingCalendarService(CrudService):
    def __init__(self, db_session: Session):
        super(HearingCalendarService, self).__init__(db_session, models.HearingCalendar)

    @check_permissions("CALENDARS_CREATE")
    def create_hearing_calendar(
        self, request: Request, request_object: schemas.HearingCalendarRequest
    ) -> schemas.HearingCalendarResponse:
        try:
            data_model: models.HearingCalendar = convert_schema_to_model(
                request_object, models.HearingCalendar
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryHearingCalendar
            ).add_to_history(
                request,
                request_object,
                "hearing_calendar_id",
                data_model.id,
                "HearingCalendar",
                "HistoryHearingCalendar",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.HearingCalendar,
                exclusions=[
                    "task_calendars",
                    "history_hearing_calendars",
                    "history_task_calendars",
                ],
            )
            self.create_related_task_calendar(request, schema_model)
            return schemas.HearingCalendarResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting Hearing Calendar. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("CALENDARS_READ")
    def read_hearing_calendar(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.HearingCalendarResponse:
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
                            f"Hearing Calendar Not Found By Id: {request_metadata.schema_model_id}!!!",  # noqa: E501
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
                    schema_class=schemas.HearingCalendar,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "task_calendars",
                        "history_hearing_calendars",
                        "history_task_calendars",
                    ],
                    extra_to_include=["task_calendars"],
                    history_to_include=["history_hearing_calendars"],
                )
                for data_model in response_data
            ]
            return schemas.HearingCalendarResponse(
                data=schema_models, metadata=response_metadata
            )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving Hearing Calendar. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("CALENDARS_UPDATE")
    def update_hearing_calendar(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.HearingCalendarRequest,
        is_restore: bool = False,
    ) -> schemas.HearingCalendarResponse:
        hearing_calendar_old = self.check_hearing_calendar_exists(
            model_id, request, is_restore
        )
        self.check_hearing_calendar_dependents_statuses(
            request, request_object.component_status_id, hearing_calendar_old
        )

        try:
            data_model: models.HearingCalendar = convert_schema_to_model(
                request_object, models.HearingCalendar
            )
            data_model = self.update(model_id, data_model, is_restore)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryHearingCalendar
            ).add_to_history(
                request,
                request_object,
                "hearing_calendar_id",
                data_model.id,
                "HearingCalendar",
                "HistoryHearingCalendar",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.HearingCalendar,
                exclusions=[
                    "task_calendars",
                    "history_hearing_calendars",
                    "history_task_calendars",
                ],
            )
            return schemas.HearingCalendarResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating Hearing Calendar By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("CALENDARS_DELETE")
    def delete_hearing_calendar(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.HearingCalendarResponse:
        hearing_calendar_old = self.check_hearing_calendar_exists(
            model_id, request, is_hard_delete
        )
        if hearing_calendar_old.task_calendars:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete Hearing Calendar {model_id}, There are Linked Task Calendars!",  # noqa: E501
            )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryHearingCalendar
            ).delete_history_before_delete_object(
                models.HistoryHearingCalendar.__tablename__,
                "hearing_calendar_id",
                model_id,
                "HearingCalendar",
                "HistoryHearingCalendar",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryHearingCalendar
            ).add_to_history(
                request,
                hearing_calendar_old,
                "hearing_calendar_id",
                model_id,
                "HearingCalendar",
                "HistoryHearingCalendar",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.HearingCalendarResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting Hearing Calendar By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def create_related_task_calendar(
        self, request: Request, hearing_calendar: schemas.HearingCalendar
    ):
        task_date_diff: int = (
            HEARING_TO_TASK_CALENDAR_DATE.get(hearing_calendar.hearing_type.name)
            or DEFAULT_HEARING_TO_TASK_CALENDAR_DATE
        )
        task_date: datetime = hearing_calendar.hearing_date - timedelta(
            days=task_date_diff
        )
        due_date: datetime = hearing_calendar.hearing_date - timedelta(days=3)
        current_date = datetime.now()
        if task_date < current_date:
            task_date = current_date

        task_calendar_request = schemas.TaskCalendarRequest(
            task_date=task_date,
            due_date=due_date,
            task_type_id=TASK_ID_DUE_AT_HEARING,
            hearing_calendar_id=hearing_calendar.id,
            status=hearing_calendar.status,
        )
        get_calendar_service(
            schemas.CalendarServiceRegistry.TASK_CALENDAR, db_session=self.db_session
        ).create_task_calendar(request, task_calendar_request)

    def check_hearing_calendar_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ) -> schemas.HearingCalendar:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id,
            is_include_extra=True,
            is_include_deleted=is_include_deleted,
        )
        hearing_calendar_response = self.read_hearing_calendar(
            request, request_metadata
        )
        if not hearing_calendar_response or not hearing_calendar_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Hearing Calendar Not Found By Id: {model_id}!!!",
            )
        return hearing_calendar_response.data[0]

    def check_hearing_calendar_dependents_statuses(
        self,
        request: Request,
        status_new: int,
        hearing_calendar_old: schemas.HearingCalendar,
    ):
        if hearing_calendar_old.task_calendars:
            status_old = hearing_calendar_old.component_status_id
            calendar_active_statuses = get_ref_types_service(
                service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
                db_session=self.db_session,
            ).get_component_status(
                request,
                schemas.ComponentStatusNames.CALENDARS,
                schemas.ComponentStatusTypes.ACTIVE,
            )
            active_status_ids = [
                component_status.id for component_status in calendar_active_statuses
            ]

            if status_new != status_old and status_new not in active_status_ids:
                if check_active_component_status(
                    hearing_calendar_old.task_calendars, active_status_ids
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update Hearing Calendar {hearing_calendar_old.id} Status to {status_new}, There are Active Task Calendars!",  # noqa: E501
                    )


class TaskCalendarService(CrudService):
    def __init__(self, db_session: Session):
        super(TaskCalendarService, self).__init__(db_session, models.TaskCalendar)

    @check_permissions("CALENDARS_CREATE")
    def create_task_calendar(
        self, request: Request, request_object: schemas.TaskCalendarRequest
    ) -> schemas.TaskCalendarResponse:
        try:
            data_model: models.TaskCalendar = convert_schema_to_model(
                request_object, models.TaskCalendar
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryTaskCalendar
            ).add_to_history(
                request,
                request_object,
                "task_calendar_id",
                data_model.id,
                "TaskCalendar",
                "HistoryTaskCalendar",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.TaskCalendar,
                exclusions=[
                    "history_task_calendars",
                ],
            )
            return schemas.TaskCalendarResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting Task Calendar. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("CALENDARS_READ")
    def read_task_calendar(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.TaskCalendarResponse:
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
                            f"Task Calendar Not Found By Id: {request_metadata.schema_model_id}!!!",  # noqa: E501
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
                    schema_class=schemas.TaskCalendar,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "history_task_calendars",
                    ],
                    history_to_include=["history_task_calendars"],
                )
                for data_model in response_data
            ]
            return schemas.TaskCalendarResponse(
                data=schema_models, metadata=response_metadata
            )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving Task Calendar. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("CALENDARS_UPDATE")
    def update_task_calendar(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.TaskCalendarRequest,
        is_restore: bool = False,
    ) -> schemas.TaskCalendarResponse:
        self.check_task_calendar_exists(model_id, request, is_restore)

        try:
            data_model: models.TaskCalendar = convert_schema_to_model(
                request_object, models.TaskCalendar
            )
            data_model = self.update(model_id, data_model, is_restore)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryTaskCalendar
            ).add_to_history(
                request,
                request_object,
                "task_calendar_id",
                data_model.id,
                "TaskCalendar",
                "HistoryTaskCalendar",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.TaskCalendar,
                exclusions=[
                    "history_task_calendars",
                ],
            )
            return schemas.TaskCalendarResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating Task Calendar By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("CALENDARS_DELETE")
    def delete_task_calendar(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.TaskCalendarResponse:
        task_calendar_old = self.check_task_calendar_exists(
            model_id, request, is_hard_delete
        )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryTaskCalendar
            ).delete_history_before_delete_object(
                models.HistoryTaskCalendar.__tablename__,
                "task_calendar_id",
                model_id,
                "TaskCalendar",
                "HistoryTaskCalendar",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryTaskCalendar
            ).add_to_history(
                request,
                task_calendar_old,
                "task_calendar_id",
                model_id,
                "TaskCalendar",
                "HistoryTaskCalendar",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.TaskCalendarResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting Task Calendar By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_task_calendar_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ) -> schemas.TaskCalendar:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id,
            is_include_extra=True,
            is_include_deleted=is_include_deleted,
        )
        task_calendar_response = self.read_task_calendar(request, request_metadata)
        if not task_calendar_response or not task_calendar_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Task Calendar Not Found By Id: {model_id}!!!",
            )
        return task_calendar_response.data[0]


def get_calendar_service(
    service_type: schemas.CalendarServiceRegistry, db_session: Session
) -> HearingCalendarService | TaskCalendarService:
    service_registry = {
        schemas.CalendarServiceRegistry.HEARING_CALENDAR: HearingCalendarService,
        schemas.CalendarServiceRegistry.TASK_CALENDAR: TaskCalendarService,
    }
    return service_registry.get(service_type)(db_session)
