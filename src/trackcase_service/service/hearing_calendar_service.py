from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import HearingCalendar as HearingCalendarModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import HearingCalendar as HearingCalendarSchema
from .schemas import HearingCalendarRequest, HearingCalendarResponse


class HearingCalendarService(CrudService):
    def __init__(self, db_session: Session):
        super(HearingCalendarService, self).__init__(db_session, HearingCalendarModel)

    def create_one_hearing_calendar(
        self, request: Request, request_object: HearingCalendarRequest
    ) -> HearingCalendarResponse:
        try:
            data_model: HearingCalendarModel = copy_objects(
                request_object, HearingCalendarModel
            )
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting HearingCalendar. Please Try Again!!!",
                str(ex),
            )

    def read_one_hearing_calendar(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> HearingCalendarResponse:
        try:
            data_model: HearingCalendarModel = super().read_one(model_id)
            if data_model:
                schema_model: HearingCalendarSchema = _convert_model_to_schema(
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

    def read_all_hearing_calendars(
        self, request: Request, is_include_extras: bool
    ) -> HearingCalendarResponse:
        try:
            data_models: List[HearingCalendarModel] = super().read_all()
            schema_models: List[HearingCalendarSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving HearingCalendars. Please Try Again!!!",
                str(ex),
            )

    def update_one_hearing_calendar(
        self, model_id: int, request: Request, request_object: HearingCalendarRequest
    ) -> HearingCalendarResponse:
        hearing_calendar_response = self.read_one_hearing_calendar(
            model_id, request, False
        )

        if not (
            hearing_calendar_response and hearing_calendar_response.hearing_calendars
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: HearingCalendarModel = copy_objects(
                request_object, HearingCalendarModel
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

    def delete_one_hearing_calendar(
        self, model_id: int, request: Request
    ) -> HearingCalendarResponse:
        hearing_calendar_response = self.read_one_hearing_calendar(
            model_id, request, False
        )

        if not (
            hearing_calendar_response and hearing_calendar_response.hearing_calendars
        ):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return HearingCalendarResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_hearing_calendar_service(db_session: Session) -> HearingCalendarService:
    return HearingCalendarService(db_session)


def get_response_single(single: HearingCalendarSchema) -> HearingCalendarResponse:
    return HearingCalendarResponse(hearing_calendars=[single])


def get_response_multiple(
    multiple: list[HearingCalendarSchema],
) -> HearingCalendarResponse:
    return HearingCalendarResponse(hearing_calendars=multiple)


def _convert_model_to_schema(
    data_model: HearingCalendarModel, is_include_extras: bool = False
) -> HearingCalendarSchema:
    data_schema = HearingCalendarSchema(
        id=data_model.id,
        created=data_model.created,
        modified=data_model.modified,
        hearing_date=data_model.hearing_date,
        hearing_type_id=data_model.hearing_type_id,
        court_case_id=data_model.court_case_id,
    )
    if is_include_extras:
        data_schema.hearing_type = data_model.hearing_type
        data_schema.court_case = data_model.court_case
        data_schema.task_calendars = data_model.task_calendars
    return data_schema
