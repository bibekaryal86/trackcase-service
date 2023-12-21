from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.case_type_service import get_case_type_service
from src.trackcase_service.service.schemas import CaseTypeRequest, CaseTypeResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/case_types", tags=["CaseTypes"])


@router.get("/", response_model=CaseTypeResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_case_type_service(db_session).read_all_case_types(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{case_type_id}", response_model=CaseTypeResponse, status_code=HTTPStatus.OK
)
def find_one(
    case_type_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    case_type_response: CaseTypeResponse = get_case_type_service(
        db_session
    ).read_one_case_type(
        case_type_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if case_type_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"CaseType Not Found By Id: {case_type_id}!!!",
        )
    return case_type_response


@router.post("/", response_model=CaseTypeResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    case_type_request: CaseTypeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_case_type_service(db_session).create_one_case_type(
        request, case_type_request
    )


@router.delete(
    "/{case_type_id}", response_model=CaseTypeResponse, status_code=HTTPStatus.OK
)
def delete_one(
    case_type_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_case_type_service(db_session).delete_one_case_type(case_type_id, request)


@router.put(
    "/{case_type_id}", response_model=CaseTypeResponse, status_code=HTTPStatus.OK
)
def update_one(
    case_type_id: int,
    request: Request,
    case_type_request: CaseTypeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_case_type_service(db_session).update_one_case_type(
        case_type_id, request, case_type_request
    )
