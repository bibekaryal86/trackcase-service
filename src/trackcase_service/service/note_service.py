import logging
from http import HTTPStatus
from typing import Type, TypeVar

from fastapi import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Base
from src.trackcase_service.utils import logger
from src.trackcase_service.utils.commons import get_err_msg, raise_http_exception
from src.trackcase_service.utils.convert import convert_request_schema_to_model

ModelBase = TypeVar("ModelBase", bound=Base)
log = logger.Logger(logging.getLogger(__name__), __name__)


class NoteService(CrudService):
    def __init__(self, db_session: Session, db_model: Type[ModelBase]):
        super(NoteService, self).__init__(db_session, db_model)

    def insert_note(
        self,
        note_schema: BaseModel,
        note_model_class: Type[ModelBase],
    ):
        try:
            note_data_model = convert_request_schema_to_model(
                note_schema, note_model_class
            )
            super().create(note_data_model)
        except Exception as ex:
            err_msg = f"Something went wrong inserting {note_model_class}!!!"
            log.error(err_msg)
            log.error(str(ex))
            raise Exception(err_msg)

    def update_note(
        self,
        note_id: int,
        request: Request,
        note_schema: BaseModel,
        note_model_class: Type[ModelBase],
    ):
        note = self.read_one(note_id)
        if not note:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Note Not Found By Id: {note_id}!!!",
            )

        try:
            note_data_model = convert_request_schema_to_model(
                note_schema, note_model_class
            )
            super().update(note_id, note_data_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating {note_schema_class} By Id: {note_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_note(self, note_id: int, request: Request):
        note = self.read_one(note_id)
        if not note:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Note Not Found By Id: {note_id}!!!",
            )

        try:
            super().delete(note_id)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Note By Id: {note_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_note_service(db_session: Session, db_model: Type[ModelBase]) -> NoteService:
    return NoteService(db_session, db_model)
