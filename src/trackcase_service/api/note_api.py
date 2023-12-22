import http
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.note_service import get_note_service
from src.trackcase_service.utils.commons import validate_http_basic_credentials, raise_http_exception
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/notes", tags=["Notes"])


@router.post("/{note_object_type}/", response_model=schemas.NoteResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    note_object_type: str,
    note_request: schemas.NoteRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_model, note_model_class = _get_note_class_and_model(note_object_type, note_request)
    if note_model:
        get_note_service(db_session, note_model_class).insert_note(note_model)
        return schemas.NoteResponse(success=True)
    else:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            error="Note Table Not Found for Note Object Type",
        )


@router.put(
    "/{note_object_type}/{note_id}", response_model=schemas.NoteResponse, status_code=HTTPStatus.OK
)
def update_one(
    note_id: int,
    request: Request,
    note_object_type: str,
    note_request: schemas.NoteRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_model, note_model_class = _get_note_class_and_model(note_object_type, note_request)
    if note_model:
        get_note_service(db_session, note_model_class).update_note(
            note_id, request, note_model
        )
        return schemas.NoteResponse(success=True)
    else:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            error="Note Table Not Found for Note Object Type",
        )


@router.delete(
    "/{note_object_type}/{note_id}", response_model=schemas.NoteResponse, status_code=HTTPStatus.OK
)
def delete_one(
    note_id: int,
    note_object_type: str,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_model_class = _get_note_class(note_object_type)
    if note_model_class:
        get_note_service(db_session, note_model_class).delete_note(note_id, request)
        return schemas.NoteResponse(success=True, delete_count=1)
    else:
        raise_http_exception(
            request=request,
            sts_code=http.HTTPStatus.BAD_REQUEST,
            error="Note Table Not Found for Note Object Type",
        )


def _get_note_class(note_object_type: str):
    match note_object_type:
        case "court":
            return models.NoteCourt
        case "judge":
            return models.NoteJudge
        case "client":
            return models.NoteClient
        case "court_case":
            return models.NoteCourtCase
        case "hearing_calendar":
            return models.NoteHearingCalendar
        case "task_calendar":
            return models.NoteTaskCalendar
        case "form":
            return models.NoteForm
        case "case_collection":
            return models.NoteCaseCollection
        case "cash_collection":
            return models.NoteCashCollection


def _get_note_class_and_model(note_object_type: str, note_request: schemas.NoteRequest):
    match note_object_type:
        case "court":
            note_model = models.NoteCourt()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.court_id = note_request.note_object_id
            return note_model, models.NoteCourt
        case "judge":
            note_model = models.NoteJudge()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.judge_id = note_request.note_object_id
            return note_model, models.NoteJudge
        case "client":
            note_model = models.NoteClient()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.client_id = note_request.note_object_id
            return note_model, models.NoteClient
        case "court_case":
            note_model = models.NoteCourtCase()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.court_case_id = note_request.note_object_id
            return note_model, models.NoteCourtCase
        case "hearing_calendar":
            note_model = models.NoteHearingCalendar()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.hearing_calendar_id = note_request.note_object_id
            return note_model, models.NoteHearingCalendar
        case "task_calendar":
            note_model = models.NoteTaskCalendar()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.task_calendar_id = note_request.note_object_id
            return note_model, models.NoteTaskCalendar
        case "form":
            note_model = models.NoteForm()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.form_id = note_request.note_object_id
            return note_model, models.NoteForm
        case "case_collection":
            note_model = models.NoteCaseCollection()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.case_collection_id = note_request.note_object_id
            return note_model, models.NoteCaseCollection
        case "cash_collection":
            note_model = models.NoteCashCollection()
            note_model.user_name = note_request.user_name
            note_model.note = note_request.note
            note_model.cash_collection_id = note_request.note_object_id
            return note_model, models.NoteCashCollection
