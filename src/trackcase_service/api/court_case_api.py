from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.service.court_case_service import get_court_case_service
from src.trackcase_service.service.schemas import CourtCaseRequest, CourtCaseResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/court_cases", tags=["CourtCases"])


@router.get("/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_court_case_service().read_all_court_cases(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{court_case_id}/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK
)
def find_one(
    court_case_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    court_case_response: CourtCaseResponse = (
        get_court_case_service().read_one_court_case(
            court_case_id,
            request,
            is_include_extra,
            is_include_history,
        )
    )
    if court_case_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"CourtCase Not Found By Id: {court_case_id}!!!",
        )
    return court_case_response


@router.post("/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    court_case_request: CourtCaseRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_court_case_service().create_one_court_case(request, court_case_request)


@router.delete(
    "/{court_case_id}/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK
)
def delete_one(
    court_case_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_court_case_service().delete_one_court_case(court_case_id, request)


@router.put(
    "/{court_case_id}/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK
)
def update_one(
    court_case_id: int,
    request: Request,
    court_case_request: CourtCaseRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_court_case_service().update_one_court_case(
        court_case_id, request, court_case_request
    )
