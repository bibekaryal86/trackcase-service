from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.data_import import (
    get_courts_import_service,
    get_judges_import_service,
)

router = APIRouter(prefix="/import", tags=["Import Data from Various Web Sources"])


@router.get(
    "/courts",
    status_code=HTTPStatus.OK,
)
def import_courts(
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    get_courts_import_service(db_session, request).import_courts()
    return {"scrape": "successful"}


@router.get(
    "/judges",
    status_code=HTTPStatus.OK,
)
def import_judges(
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    get_judges_import_service(db_session, request).import_judges()
    return {"scrape": "successful"}
