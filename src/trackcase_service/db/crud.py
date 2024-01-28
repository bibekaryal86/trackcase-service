from typing import Any, Dict, List, Type, TypeVar

from sqlalchemy import TextClause, asc, desc, func

from src.trackcase_service.db.models import Base
from src.trackcase_service.db.session import get_db_session

ModelBase = TypeVar("ModelBase", bound=Base)


class CrudService:
    def __init__(self, db_model: Type[ModelBase]):
        self.db_model = db_model

    def execute_raw_query(self, query: TextClause):
        try:
            with get_db_session() as db_session:
                result = db_session.execute(query)
                db_session.commit()
                return result
        except Exception as ex:
            db_session.rollback()
            raise ex

    def create(self, model_data: ModelBase) -> ModelBase:
        setattr(model_data, "created", func.now())
        setattr(model_data, "modified", func.now())

        try:
            with get_db_session() as db_session:
                db_session.add(model_data)
                db_session.commit()
                db_session.refresh(model_data)
                return model_data
        except Exception as ex:
            db_session.rollback()
            raise ex

    def read_one(self, model_id: int) -> ModelBase:
        try:
            with get_db_session() as db_session:
                return (
                    db_session.query(self.db_model)
                    .filter(self.db_model.id == model_id)
                    .first()
                )
        except Exception as ex:
            db_session.rollback()
            raise ex

    def read_all(
        self,
        sort_config: dict = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> List[ModelBase]:
        try:
            with get_db_session() as db_session:
                query = db_session.query(self.db_model)
                if sort_config:
                    order_by_conditions = [
                        asc(col) if direction.lower() == "asc" else desc(col)
                        for col, direction in sort_config.items()
                    ]
                    query = query.order_by(*order_by_conditions)
                result = query.offset(skip).limit(limit).all()
                db_session.commit()
                return result
        except Exception as ex:
            db_session.rollback()
            raise ex

    def read_many(self, sort_map: dict, **kwargs: Dict[str, Any]) -> List[ModelBase]:
        try:
            with get_db_session() as db_session:
                query = db_session.query(self.db_model)
                order_by_conditions = [
                    asc(col) if direction.lower() == "asc" else desc(col)
                    for col, direction in sort_map.items()
                ]
                query = query.order_by(*order_by_conditions)
                for column, value in kwargs.items():
                    query = query.filter(getattr(self.db_model, column) == value)
                result = query.all()
                db_session.commit()
                return result
        except Exception as ex:
            db_session.rollback()
            raise ex

    def update(self, model_id: int, model_data: ModelBase) -> ModelBase:
        try:
            with get_db_session() as db_session:
                db_record = db_session.query(self.db_model).get(model_id)
                # exists check done in controller/api for better messaging, so no need again
                db_record = _copy_key_values(model_data, db_record)
                setattr(db_record, "modified", func.now())
                db_session.commit()
                db_session.refresh(db_record)
                return db_record
        except Exception as ex:
            db_session.rollback()
            raise ex

    def delete(self, model_id: int) -> bool:
        try:
            with get_db_session() as db_session:
                db_record = db_session.query(self.db_model).get(model_id)
                # exists check done in controller/api for better messaging, so no need again
                db_session.delete(db_record)
                db_session.commit()
                return True
        except Exception as ex:
            db_session.rollback()
            raise ex


def _copy_key_values(model_data, db_record):
    # Get a list of attributes for the db_record object
    db_attributes_and_types = {
        attr: type(getattr(db_record, attr))
        for attr in dir(db_record)
        if not callable(getattr(db_record, attr)) and not attr.startswith("_")
    }

    for attr_name, attr_type in db_attributes_and_types.items():
        attr_value = getattr(model_data, attr_name)
        if _is_should_set_attr_value(model_data, attr_name, attr_value, attr_type):
            setattr(db_record, attr_name, attr_value)
    return db_record


def _is_should_set_attr_value(model_data, attr_name, attr_value, attr_type) -> bool:
    auto_generated_attributes = ["id", "created", "modified", "metadata", "registry"]
    if hasattr(model_data, attr_name):
        if attr_name not in auto_generated_attributes:
            if not isinstance(attr_value, list):
                if attr_value is None:
                    return attr_type == str or attr_type == int or attr_type == bool
                else:
                    return True
    return False
