from typing import List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session
from trackcase_service.db.models import Base

ModelBase = TypeVar("ModelBase", bound=Base)
SchemaBase = TypeVar("SchemaBase", bound=BaseModel)


class CrudService:
    def __init__(self, db_session: Session, db_model: Type[ModelBase]):
        self.db_model = db_model
        self.db_session = db_session

    def get_by_id(self, model_id: int) -> SchemaBase:
        return (
            self.db_session.query(self.db_model)
            .filter(self.db_model.id == model_id)
            .first()
        )

    def read_all(self, skip: int = 0, limit: int = 1000) -> List[SchemaBase]:
        return self.db_session.query(self.db_model).offset(skip).limit(limit).all()

    def delete(self, model_id: int) -> bool:
        db_record = self.db_session.query(self.db_model).get(model_id)

        if db_record is None:
            return False

        self.db_session.delete(db_record)
        self.db_session.commit()
        return True
