from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service.schemas import TaskTypeRequest, TaskTypeResponse
from src.trackcase_service.service.task_type_service import get_task_type_service
from src.trackcase_service.utils.commons import (
    raise_http_exception,
)

router = APIRouter(prefix="/trackcase-service/task_types", tags=["TaskTypes"])


@router.get("/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_task_type_service(db_session).read_all_task_types(
        request, is_include_extra, is_include_history
    )


@router.get(
    "/{task_type_id}/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK
)
def find_one(
    task_type_id: int,
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    db_session: Session = Depends(get_db_session),
):
    task_type_response: TaskTypeResponse = get_task_type_service(
        db_session
    ).read_one_task_type(
        task_type_id,
        request,
        is_include_extra,
        is_include_history,
    )
    if task_type_response is None:
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"TaskType Not Found By Id: {task_type_id}!!!",
        )
    return task_type_response


@router.post("/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK)
def insert_one(
    request: Request,
    task_type_request: TaskTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_task_type_service(db_session).create_one_task_type(
        request, task_type_request
    )


@router.delete(
    "/{task_type_id}/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK
)
def delete_one(
    task_type_id: int,
    request: Request,
    db_session: Session = Depends(get_db_session),
):
    return get_task_type_service(db_session).delete_one_task_type(task_type_id, request)


@router.put(
    "/{task_type_id}/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK
)
def update_one(
    task_type_id: int,
    request: Request,
    task_type_request: TaskTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_task_type_service(db_session).update_one_task_type(
        task_type_id, request, task_type_request
    )
