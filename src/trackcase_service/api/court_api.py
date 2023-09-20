from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
from trackcase_service.db.session import get_db_session
from trackcase_service.service.court_service import (
    get_court_service,
    get_response_multiple,
    get_response_single,
)
from trackcase_service.service.schemas import CourtResponse
from trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/courts", tags=["Courts"])


@router.get("/", response_model=CourtResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    try:
        courts = get_court_service(db_session).get_all()
        return get_response_multiple(courts)
    except Exception as ex:
        raise_http_exception(
            request,
            HTTPStatus.SERVICE_UNAVAILABLE,
            "Error Retrieving Courts. Please Try Again!!!",
            str(ex),
        )


@router.get("/{court_id}", response_model=CourtResponse, status_code=HTTPStatus.OK)
def find(
    court_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    try:
        court = get_court_service(db_session).get_by_id(court_id)
        if court is None:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Court Not Found By Id: {court_id}!!!",
                f"Court Not Found By Id: {court_id}!!!",
            )
        return get_response_single(court)
    except Exception as ex:
        raise_http_exception(
            request,
            HTTPStatus.SERVICE_UNAVAILABLE,
            f"Error Retrieving Court By Id: {court_id}. Please Try Again!!!",
            str(ex),
        )
