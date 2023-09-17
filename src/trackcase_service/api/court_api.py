import http

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from trackcase_service.db.session import get_db_session
from trackcase_service.service.court_service import (
    get_court_service,
    get_response_error,
    get_response_multiple,
    get_response_single,
)
from trackcase_service.service.schemas import Court, CourtResponse
from trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/courts", tags=["Courts"])


@router.get("/", response_model=CourtResponse, status_code=http.HTTPStatus.OK)
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
        msg = "Error Retrieving Courts List. Please Try Again!!!"
        err_msg = str(ex)
        raise_http_exception(
            request,
            http.HTTPStatus.SERVICE_UNAVAILABLE,
            detail=get_response_error(msg, err_msg),
        )


@router.get("/{court_id}", response_model=CourtResponse, status_code=http.HTTPStatus.OK)
def find(
    court_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    try:
        court = get_court_service(db_session).get_by_id(court_id)
        return get_response_single(court)
    except Exception as ex:
        msg = "Error Retrieving Court By Id. Please Try Again!!!"
        err_msg = str(ex)
        raise_http_exception(
            request,
            http.HTTPStatus.SERVICE_UNAVAILABLE,
            detail=get_response_error(msg, err_msg),
        )
