from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.service.judge_service import get_judge_service
from src.trackcase_service.service.schemas import JudgeRequest, JudgeResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/judges", tags=["Judges"])


@router.get("/", response_model=JudgeResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_judge_service().read_all_judges(
        request, is_include_extra, is_include_history
    )


@router.get("/{judge_id}/", response_model=JudgeResponse, status_code=HTTPStatus.OK)
def find_one(
    judge_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    judge_response: JudgeResponse = get_judge_service().read_one_judge(
        judge_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if judge_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"Judge Not Found By Id: {judge_id}!!!",
        )
    return judge_response


@router.post("/", response_model=JudgeResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    judge_request: JudgeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_judge_service().create_one_judge(request, judge_request)


@router.delete("/{judge_id}/", response_model=JudgeResponse, status_code=HTTPStatus.OK)
def delete_one(
    judge_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_judge_service().delete_one_judge(judge_id, request)


@router.put("/{judge_id}/", response_model=JudgeResponse, status_code=HTTPStatus.OK)
def update_one(
    judge_id: int,
    request: Request,
    judge_request: JudgeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_judge_service().update_one_judge(judge_id, request, judge_request)
