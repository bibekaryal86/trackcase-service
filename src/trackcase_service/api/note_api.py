import http
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.service import schemas
from src.trackcase_service.service.note_service import get_note_service
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security
from src.trackcase_service.utils.convert import convert_note_request_to_note_model

router = APIRouter(prefix="/trackcase-service/notes", tags=["Notes"])


@router.post(
    "/{note_object_type}/",
    response_model=schemas.NoteResponse,
    status_code=HTTPStatus.OK,
)
def insert_one(
    request: Request,
    note_object_type: str,
    note_request: schemas.NoteRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_model_class, note_model = convert_note_request_to_note_model(
        note_object_type, note_request
    )
    if note_model:
        get_note_service(note_model_class).insert_note(note_model)
        return schemas.NoteResponse(success=True)
    else:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            error="Note Table Not Found for Note Object Type",
        )


@router.put(
    "/{note_object_type}/{note_id}/",
    response_model=schemas.NoteResponse,
    status_code=HTTPStatus.OK,
)
def update_one(
    note_id: int,
    request: Request,
    note_object_type: str,
    note_request: schemas.NoteRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_model_class, note_model = convert_note_request_to_note_model(
        note_object_type, note_request
    )
    if note_model:
        get_note_service(note_model_class).update_note(note_id, request, note_model)
        return schemas.NoteResponse(success=True)
    else:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            error="Note Table Not Found for Note Object Type",
        )


@router.delete(
    "/{note_object_type}/{note_id}/",
    response_model=schemas.NoteResponse,
    status_code=HTTPStatus.OK,
)
def delete_one(
    note_id: int,
    note_object_type: str,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_model_class, note_model = convert_note_request_to_note_model(
        note_object_type,
    )
    if note_model_class:
        get_note_service(note_model_class).delete_note(note_id, request)
        return schemas.NoteResponse(success=True, delete_count=1)
    else:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            error="Note Table Not Found for Note Object Type",
        )
