from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import HearingCalendar as HearingCalendarModel
from src.trackcase_service.db.models import (
    HistoryHearingCalendar as HistoryHearingCalendarModel,
)
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import (
    HearingCalendar as HearingCalendarSchema,
)
from src.trackcase_service.service.schemas import (
    HearingCalendarRequest,
    HearingCalendarResponse,
)
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import (
    convert_hearing_calendar_model_to_schema,
    convert_request_schema_to_model,
)


class HearingCalendarService(CrudService):
    def __init__(self, db_session: Session):
        super(HearingCalendarService, self).__init__(db_session, HearingCalendarModel)

    def create_one_hearing_calendar(
        self, request: Request, request_object: HearingCalendarRequest
    ) -> HearingCalendarResponse:
        try:
            data_model: HearingCalendarModel = convert_request_schema_to_model(
                request_object, HearingCalendarModel
            )
            data_model = super().create(data_model)
            _handle_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_hearing_calendar_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting HearingCalendar. Please Try Again!!!", str(ex)
                ),
            )

    def read_one_hearing_calendar(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> HearingCalendarResponse:
        try:
            data_model: HearingCalendarModel = super().read_one(model_id)
            if data_model:
                schema_model: HearingCalendarSchema = (
                    convert_hearing_calendar_model_to_schema(
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
                    f"Error Retrieving HearingCalendar By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_hearing_calendars(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> HearingCalendarResponse:
        try:
            data_models: List[HearingCalendarModel] = super().read_all(
                sort_direction="desc", sort_by="hearing_date"
            )
            schema_models: List[HearingCalendarSchema] = [
                convert_hearing_calendar_model_to_schema(
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
                    "Error Retrieving HearingCalendars. Please Try Again!!!", str(ex)
                ),
            )

    def update_one_hearing_calendar(
        self, model_id: int, request: Request, request_object: HearingCalendarRequest
    ) -> HearingCalendarResponse:
        hearing_calendar_response = self.read_one_hearing_calendar(model_id, request)

        if not (
            hearing_calendar_response and hearing_calendar_response.hearing_calendars
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"HearingCalendar Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: HearingCalendarModel = convert_request_schema_to_model(
                request_object, HearingCalendarModel
            )
            data_model = super().update(model_id, data_model)
            _handle_history(self.db_session, request, model_id, request_object)
            schema_model = convert_hearing_calendar_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating HearingCalendar By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_hearing_calendar(
        self, model_id: int, request: Request
    ) -> HearingCalendarResponse:
        hearing_calendar_response = self.read_one_hearing_calendar(model_id, request)

        if not (
            hearing_calendar_response and hearing_calendar_response.hearing_calendars
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"HearingCalendar Not Found By Id: {model_id}!!!",
            )

        try:
            _handle_history(self.db_session, request, model_id, is_delete=True)
            super().delete(model_id)
            return HearingCalendarResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting HearingCalendar By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_hearing_calendar_service(db_session: Session) -> HearingCalendarService:
    return HearingCalendarService(db_session)


def get_response_single(single: HearingCalendarSchema) -> HearingCalendarResponse:
    return HearingCalendarResponse(hearing_calendars=[single])


def get_response_multiple(
    multiple: list[HearingCalendarSchema],
) -> HearingCalendarResponse:
    return HearingCalendarResponse(hearing_calendars=multiple)


def _handle_history(
    db_session: Session,
    request: Request,
    hearing_calendar_id: int,
    request_object: HearingCalendarRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryHearingCalendarModel)
    if is_delete:
        history_service.delete_history_before_delete_object(
            HistoryHearingCalendarModel.__tablename__,
            "hearing_calendar_id",
            hearing_calendar_id,
            "HearingCalendar",
            "HistoryHearingCalendar",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "hearing_calendar_id",
            hearing_calendar_id,
            "HearingCalendar",
            "HistoryHearingCalendar",
        )
