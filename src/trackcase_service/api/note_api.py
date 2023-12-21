from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.note_service import get_note_service
from src.trackcase_service.utils.commons import validate_http_basic_credentials
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/notes", tags=["Notes"])


@router.post("/", response_model=schemas.NoteResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    note_request: schemas.NoteRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_schema, note_model_class = _get_note_schema_model_class(note_request)
    return get_note_service(db_session, note_model_class).insert_note(
        note_schema, note_model_class
    )


@router.put(
    "/{note_id}", response_model=schemas.NoteResponse, status_code=HTTPStatus.OK
)
def update_one(
    note_id: int,
    request: Request,
    note_request: schemas.NoteRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_schema, note_model_class = _get_note_schema_model_class(note_request)
    return get_note_service(db_session, note_model_class).update_note(
        note_id, request, note_schema, note_model_class
    )


@router.delete(
    "/{note_id}", response_model=schemas.NoteResponse, status_code=HTTPStatus.OK
)
def delete_one(
    note_id: int,
    request: Request,
    note_request: schemas.NoteRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
    db_session: Session = Depends(get_db_session),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    note_schema, note_model_class = _get_note_schema_model_class(note_request)
    return get_note_service(db_session, note_model_class).delete_note(note_id, request)


def _get_note_schema_model_class(note_request: schemas.NoteRequest):
    match note_request.note_object_type:
        case "court":
            return (
                schemas.NoteCourt(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    court_id=note_request.note_object_id,
                ),
                models.NoteCourt,
            )
        case "judge":
            return (
                schemas.NoteJudge(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    judge_id=note_request.note_object_id,
                ),
                models.NoteJudge,
            )
        case "client":
            return (
                schemas.NoteClient(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    client_id=note_request.note_object_id,
                ),
                models.NoteClient,
            )
        case "court_case":
            return (
                schemas.NoteCourtCase(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    court_case_id=note_request.note_object_id,
                ),
                models.NoteCourtCase,
            )
        case "hearing_calendar":
            return (
                schemas.NoteHearingCalendar(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    hearing_calendar_id=note_request.note_object_id,
                ),
                models.NoteHearingCalendar,
            )
        case "task_calendar":
            return (
                schemas.NoteTaskCalendar(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    task_calendar_id=note_request.note_object_id,
                ),
                models.NoteTaskCalendar,
            )
        case "form":
            return (
                schemas.NoteForm(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    form_id=note_request.note_object_id,
                ),
                models.NoteForm,
            )
        case "case_collection":
            return (
                schemas.NoteCaseCollection(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    case_collection_id=note_request.note_object_id,
                ),
                models.NoteCaseCollection,
            )
        case "cash_collection":
            return (
                schemas.NoteCashCollection(
                    user_name=note_request.user_name,
                    note=note_request.note,
                    cash_collection_id=note_request.note_object_id,
                ),
                models.NoteCashCollection,
            )
