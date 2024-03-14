from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.judge import get_judge_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/judges", tags=["Judges"])


@router.post(
    "/",
    response_model=schemas.JudgeResponse,
    status_code=HTTPStatus.OK,
)
def insert_judge(
    request: Request,
    judge_request: schemas.JudgeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_judge_service(db_session).create_judge(request, judge_request)


@router.get(
    "/",
    response_model=schemas.JudgeResponse,
    status_code=HTTPStatus.OK,
)
def find_judge(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_judge_service(db_session).read_judge(request, request_metadata)


@router.put(
    "/{judge_id}/",
    response_model=schemas.JudgeResponse,
    status_code=HTTPStatus.OK,
)
def modify_judge(
    judge_id: int,
    request: Request,
    judge_request: schemas.JudgeRequest,
    is_restore: bool = Query(default=False),
    db_session: Session = Depends(get_db_session),
):
    return get_judge_service(db_session).update_judge(
        judge_id, request, judge_request, is_restore
    )


@router.delete(
    "/{judge_id}/{is_hard_delete}/",
    response_model=schemas.JudgeResponse,
    status_code=HTTPStatus.OK,
)
def remove_judge(
    judge_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_judge_service(db_session).delete_judge(judge_id, is_hard_delete, request)
