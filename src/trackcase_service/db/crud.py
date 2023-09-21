from typing import List, Type, TypeVar

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

    def read_all(self, skip: int = 0, limit: int = 1000) -> List[ModelBase]:
        return self.db_session.query(self.db_model).offset(skip).limit(limit).all()

    def update(self, model_id: int, model_data: ModelBase) -> ModelBase:
        db_record = self.db_session.query(self.db_model).get(model_id)
        # exists check done in controller/api for better messaging, so no need again
        for key, value in model_data.dict().items():
            setattr(db_record, key, value)
        self.db_session.commit()
        return db_record

    def delete(self, model_id: int) -> bool:
        db_record = self.db_session.query(self.db_model).get(model_id)
        # exists check done in controller/api for better messaging, so no need again
        self.db_session.delete(db_record)
        self.db_session.commit()
        return True
