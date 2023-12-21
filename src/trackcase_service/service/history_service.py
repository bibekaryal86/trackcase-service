import logging
from typing import Type, TypeVar, Union

from fastapi import Request
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Base
from src.trackcase_service.utils import logger
from src.trackcase_service.utils.constants import USERNAME_HEADER
from src.trackcase_service.utils.convert import convert_request_schema_to_history_model

ModelBase = TypeVar("ModelBase", bound=Base)
log = logger.Logger(logging.getLogger(__name__), __name__)


class HistoryService(CrudService):
    def __init__(self, db_session: Session, db_model: Type[ModelBase]):
        super(HistoryService, self).__init__(db_session, db_model)

    def add_to_history(
        self,
        request: Request,
        request_object: BaseModel,
        history_object_id_key: str,
        history_object_id_value: Union[str, int],
        parent_type: str,
        history_type: str,
    ):
        user_name = request.headers.get(USERNAME_HEADER)
        history_data_model = convert_request_schema_to_history_model(
            request_object,
            self.db_model,
            user_name,
            history_object_id_key,
            history_object_id_value,
        )
        try:
            super().create(history_data_model)
        except Exception as ex:
            err_msg = f"{parent_type} Action Successful! BUT!! Something went wrong inserting {history_type}!!!"
            log.error(err_msg)
            log.error(str(ex))
            raise Exception(err_msg)

    def add_to_history_for_delete(
        self,
        request: Request,
        history_table_name: str,
        id_key: str,
        id_value: int,
        parent_type: str,
        history_type: str,
    ):
        user_name_value = request.headers.get(USERNAME_HEADER)
        sql = text(
            f"""INSERT INTO {history_table_name} (user_name, {id_key}) VALUES ('{user_name_value}', {id_value})"""
        )
        try:
            self.db_session.execute(sql)
        except Exception as ex:
            err_msg = f"{parent_type} Action Successful! BUT!! Something went wrong inserting {history_type}!!!"
            log.error(err_msg)
            log.error(str(ex))
            raise Exception(err_msg)


def get_history_service(
    db_session: Session, db_model: Type[ModelBase]
) -> HistoryService:
    return HistoryService(db_session, db_model)
