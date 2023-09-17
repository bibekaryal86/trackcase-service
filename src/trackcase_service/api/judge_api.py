import http

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from trackcase_service.db.session import get_db_session
from trackcase_service.service.judge_service import (
    get_judge_service,
    get_response_error,
    get_response_multiple,
    get_response_single,
)
from trackcase_service.service.schemas import Judge, JudgeResponse
from trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/judges", tags=["Judges"])


@router.get("/", response_model=JudgeResponse, status_code=http.HTTPStatus.OK)
def find_all(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    try:
        judges = get_judge_service(db_session).get_all()
        return get_response_multiple(judges)
    except Exception as ex:
        msg = "Error Retrieving Judges List. Please Try Again!!!"
        err_msg = str(ex)
        raise_http_exception(
            request,
            http.HTTPStatus.SERVICE_UNAVAILABLE,
            detail=get_response_error(msg, err_msg),
        )


@router.get("/{judge_id}", response_model=JudgeResponse, status_code=http.HTTPStatus.OK)
def find(
    judge_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    try:
        court = get_judge_service(db_session).get_by_id(judge_id)
        return get_response_single(court)
    except Exception as ex:
        msg = "Error Retrieving Judge By Id. Please Try Again!!!"
        err_msg = str(ex)
        raise_http_exception(
            request,
            http.HTTPStatus.SERVICE_UNAVAILABLE,
            detail=get_response_error(msg, err_msg),
        )
