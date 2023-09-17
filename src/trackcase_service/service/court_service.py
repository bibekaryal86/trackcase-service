from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService

from ..db.models import Court as CourtModel
from .schemas import Court as CourtSchema
from .schemas import CourtResponse


class CourtService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtService, self).__init__(db_session, CourtModel)


def get_court_service(db_session: Session) -> CourtService:
    return CourtService(db_session)


def get_response_single(single: CourtSchema) -> CourtResponse:
    if single is None:
        return CourtResponse()
    return CourtResponse(courts=[single])


def get_response_multiple(multiple: list[CourtSchema]) -> CourtResponse:
    return CourtResponse(courts=multiple)


def get_response_error(msg: str, err_msg: str) -> CourtResponse:
    return CourtResponse(msg=msg, err_msg=err_msg)
