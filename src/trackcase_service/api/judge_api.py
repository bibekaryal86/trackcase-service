from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.judge_service import (
    get_judge_service,
    get_response_multiple,
    get_response_single,
)
from src.trackcase_service.service.schemas import JudgeResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/judges", tags=["Judges"])


@router.get("/", response_model=JudgeResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    try:
        judges = get_judge_service(db_session).read_all()
        return get_response_multiple(judges)
    except Exception as ex:
        raise_http_exception(
            request,
            HTTPStatus.SERVICE_UNAVAILABLE,
            "Error Retrieving Judges List. Please Try Again!!!",
            str(ex),
        )


@router.get("/{judge_id}", response_model=JudgeResponse, status_code=HTTPStatus.OK)
def find_one(
    judge_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    try:
        judge = get_judge_service(db_session).read_one(judge_id)
        if judge is None:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Judge Not Found By Id: {judge_id}!!!",
                f"Judge Not Found By Id: {judge_id}!!!",
            )
        return get_response_single(judge)
    except Exception as ex:
        raise_http_exception(
            request,
            HTTPStatus.SERVICE_UNAVAILABLE,
            f"Error Retrieving Judge By Id: {judge_id}. Please Try Again!!!",
            str(ex),
        )
