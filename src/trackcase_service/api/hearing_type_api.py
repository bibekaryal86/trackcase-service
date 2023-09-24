from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.hearing_type_service import get_hearing_type_service
from src.trackcase_service.service.schemas import HearingTypeRequest, HearingTypeResponse
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/hearing_types", tags=["HearingTypes"])


@router.get("/", response_model=HearingTypeResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extras: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_hearing_type_service(db_session).read_all_hearing_types(request, is_include_extras)


@router.get("/{hearing_type_id}", response_model=HearingTypeResponse, status_code=HTTPStatus.OK)
def find_one(
    hearing_type_id: int,
    request: Request,
    is_include_extras: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    hearing_type_response: HearingTypeResponse = get_hearing_type_service(db_session).read_one_hearing_type(
        hearing_type_id, request, is_include_extras
    )
    if hearing_type_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"HearingType Not Found By Id: {hearing_type_id}!!!",
            f"HearingType Not Found By Id: {hearing_type_id}!!!",
        )
    return hearing_type_response


@router.post("/", response_model=HearingTypeResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    hearing_type_request: HearingTypeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_hearing_type_service(db_session).create_one_hearing_type(request, hearing_type_request)


@router.delete("/{hearing_type_id}", response_model=HearingTypeResponse, status_code=HTTPStatus.OK)
def delete_one(
    hearing_type_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_hearing_type_service(db_session).delete_one_hearing_type(hearing_type_id, request)


@router.put("/{hearing_type_id}", response_model=HearingTypeResponse, status_code=HTTPStatus.OK)
def update_one(
    hearing_type_id: int,
    request: Request,
    hearing_type_request: HearingTypeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_hearing_type_service(db_session).update_one_hearing_type(
        hearing_type_id, request, hearing_type_request
    )
