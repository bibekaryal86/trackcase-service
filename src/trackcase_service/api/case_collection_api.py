from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.case_collection_service import (
    get_case_collection_service,
)
from src.trackcase_service.service.schemas import (
    CaseCollectionRequest,
    CaseCollectionResponse,
    CaseCollectionRetrieveRequest,
)
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(
    prefix="/trackcase-service/case_collections", tags=["CaseCollections"]
)


@router.get("/", response_model=CaseCollectionResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    case_collection_retrieve_request: CaseCollectionRetrieveRequest = None,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    if case_collection_retrieve_request is None:
        return get_case_collection_service(db_session).read_all_case_collections(
            request,
            is_include_extra,
            is_include_history,
        )
    else:
        return get_case_collection_service(db_session).read_many_case_collections(
            request,
            case_collection_retrieve_request,
            is_include_extra,
            is_include_history,
        )


@router.get(
    "/{case_collection_id}/",
    response_model=CaseCollectionResponse,
    status_code=HTTPStatus.OK,
)
def find_one(
    case_collection_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    case_collection_response: CaseCollectionResponse = get_case_collection_service(
        db_session
    ).read_one_case_collection(
        case_collection_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if case_collection_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"CaseCollection Not Found By Id: {case_collection_id}!!!",
        )
    return case_collection_response


@router.post("/", response_model=CaseCollectionResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    case_collection_request: CaseCollectionRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_case_collection_service(db_session).create_one_case_collection(
        request, case_collection_request
    )


@router.delete(
    "/{case_collection_id}/",
    response_model=CaseCollectionResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    case_collection_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_case_collection_service(db_session).delete_one_case_collection(
        case_collection_id, request
    )


@router.put(
    "/{case_collection_id}/",
    response_model=CaseCollectionResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    case_collection_id: int,
    request: Request,
    case_collection_request: CaseCollectionRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_case_collection_service(db_session).update_one_case_collection(
        case_collection_id, request, case_collection_request
    )
