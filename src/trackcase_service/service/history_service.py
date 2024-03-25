import logging
from typing import Type, TypeVar, Union

from fastapi import Request
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Base
from src.trackcase_service.utils.commons import get_auth_user_token
from src.trackcase_service.utils.convert import convert_schema_to_model
from src.trackcase_service.utils.logger import Logger

log = Logger(logging.getLogger(__name__))
ModelBase = TypeVar("ModelBase", bound=Base)


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
        app_user_id = get_auth_user_token(request).get("id")
        history_data_model = convert_schema_to_model(
            request_object,
            self.db_model,
            app_user_id,
            history_object_id_key,
            history_object_id_value,
            exclusions=["id", "created", "modified"]
        )
        try:
            super().create(history_data_model)
        except Exception as ex:
            err_msg = f"{parent_type} Action Successful! BUT!! Something went wrong inserting {history_type}!!!"  # noqa: E501
            log.error(err_msg, extra=ex)
            raise Exception(err_msg)

    def delete_history_before_delete_object(
        self,
        history_table_name: str,
        id_key: str,
        id_value: int,
        parent_type: str,
        history_type: str,
    ):
        sql = text(f"""DELETE FROM {history_table_name} WHERE {id_key} = {id_value}""")
        try:
            self.db_session.execute(sql)
        except Exception as ex:
            err_msg = (
                f"Something went wrong deleting all {history_type} for {parent_type}!!!"
            )
            log.error(err_msg, extra=ex)
            raise Exception(err_msg)


def get_history_service(
    db_session: Session, db_model: Type[ModelBase]
) -> HistoryService:
    return HistoryService(db_session, db_model)
