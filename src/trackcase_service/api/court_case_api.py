from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.court_case_service import get_court_case_service
from src.trackcase_service.service.schemas import CourtCaseRequest, CourtCaseResponse
from src.trackcase_service.utils.commons import raise_http_exception

router = APIRouter(prefix="/trackcase-service/court_cases", tags=["CourtCases"])


@router.get("/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).read_all_court_cases(
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
    db_session: Session = Depends(get_db_session),
):
    court_case_response: CourtCaseResponse = get_court_case_service(
        db_session
    ).read_one_court_case(
        court_case_id,
        request,
        is_include_extra,
        is_include_history,
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
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).create_one_court_case(
        request, court_case_request
    )


@router.delete(
    "/{court_case_id}/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK
)
def delete_one(
    court_case_id: int,
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).delete_one_court_case(
        court_case_id, request
    )


@router.put(
    "/{court_case_id}/", response_model=CourtCaseResponse, status_code=HTTPStatus.OK
)
def update_one(
    court_case_id: int,
    request: Request,
    court_case_request: CourtCaseRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_court_case_service(db_session).update_one_court_case(
        court_case_id, request, court_case_request
    )
