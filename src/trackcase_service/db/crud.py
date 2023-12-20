from typing import Any, Dict, List, Type, TypeVar

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from src.trackcase_service.db.models import Base

ModelBase = TypeVar("ModelBase", bound=Base)


class CrudService:
    def __init__(self, db_session: Session, db_model: Type[ModelBase]):
        self.db_model = db_model
        self.db_session = db_session

    def create(self, model_data: ModelBase) -> ModelBase:
        self.db_session.add(model_data)
        self.db_session.commit()
        self.db_session.refresh(model_data)
        return model_data

    def read_one(self, model_id: int) -> ModelBase:
        return (
            self.db_session.query(self.db_model)
            .filter(self.db_model.id == model_id)
            .first()
        )

    def read_all(
        self,
        sort_direction: str = None,
        sort_by: str = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> List[ModelBase]:
        if sort_direction and sort_by:
            if sort_direction == "asc":
                return (
                    self.db_session.query(self.db_model)
                    .order_by(asc(sort_by))
                    .offset(skip)
                    .limit(limit)
                    .all()
                )
            return (
                self.db_session.query(self.db_model)
                .order_by(desc(sort_by))
                .offset(skip)
                .limit(limit)
                .all()
            )
        return self.db_session.query(self.db_model).offset(skip).limit(limit).all()

    def read_many(
        self, sort_direction: str, sort_by: str, **kwargs: Dict[str, Any]
    ) -> List[ModelBase]:
        if sort_direction and sort_by:
            if sort_direction == "asc":
                query = self.db_session.query(self.db_model).order_by(asc(sort_by))
            else:
                query = self.db_session.query(self.db_model).order_by(desc(sort_by))
        else:
            query = self.db_session.query(self.db_model)

        for column, value in kwargs.items():
            query = query.filter(getattr(self.db_model, column) == value)

        return query.all()

    def update(self, model_id: int, model_data: ModelBase) -> ModelBase:
        db_record = self.db_session.query(self.db_model).get(model_id)
        # exists check done in controller/api for better messaging, so no need again
        db_record = _copy_key_values(model_data, db_record)
        self.db_session.commit()
        self.db_session.refresh(db_record)
        return db_record

    def delete(self, model_id: int) -> bool:
        db_record = self.db_session.query(self.db_model).get(model_id)
        # exists check done in controller/api for better messaging, so no need again
        self.db_session.delete(db_record)
        self.db_session.commit()
        return True


def _copy_key_values(model_data, db_record):
    auto_generated_attributes = ["id", "created", "modified", "metadata", "registry"]
    # Get a list of attributes for the db_record object
    model_attributes = [
        attr
        for attr in dir(model_data)
        if not callable(getattr(model_data, attr)) and not attr.startswith("_")
    ]

    for attr_name in model_attributes:
        attr_value = getattr(model_data, attr_name)
        if (
            attr_value is not None
            and hasattr(db_record, attr_name)
            and attr_name not in auto_generated_attributes
            and not isinstance(attr_value, list)
        ):
            setattr(db_record, attr_name, attr_value)

    return db_record
