from typing import List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class CrudService:
    def __init__(self, db_session: Session, db_model: Type[ModelType]):
        self.db_model = db_model
        self.db_session = db_session

    def get_by_id(self, model_id: int) -> BaseSchema:
        return (
            self.db_session.query(self.db_model)
            .filter(self.db_model.id == model_id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 1000) -> List[BaseSchema]:
        return self.db_session.query(self.db_model).offset(skip).limit(limit).all()
