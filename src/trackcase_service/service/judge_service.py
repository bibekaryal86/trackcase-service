from sqlalchemy.orm import Session

from trackcase_service.db.crud import CrudService
from trackcase_service.db.models import Judge as JudgeModel

from .schemas import Judge as JudgeSchema
from .schemas import JudgeResponse


class JudgeService(CrudService):
    def __init__(self, db_session: Session):
        super(JudgeService, self).__init__(db_session, JudgeModel)


def get_judge_service(db_session: Session) -> JudgeService:
    return JudgeService(db_session)


def get_response_single(single: JudgeSchema) -> JudgeResponse:
    return JudgeResponse(judges=[single])


def get_response_multiple(multiple: list[JudgeSchema]) -> JudgeResponse:
    return JudgeResponse(judges=multiple)
