from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBasicCredentials

from src.trackcase_service.service.schemas import TaskTypeRequest, TaskTypeResponse
from src.trackcase_service.service.task_type_service import get_task_type_service
from src.trackcase_service.utils.commons import (
    raise_http_exception,
    validate_http_basic_credentials,
)
from src.trackcase_service.utils.constants import http_basic_security

router = APIRouter(prefix="/trackcase-service/task_types", tags=["TaskTypes"])


@router.get("/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK)
def find_all(
    request: Request,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_type_service().read_all_task_types(
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
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    task_type_response: TaskTypeResponse = get_task_type_service().read_one_task_type(
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
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_type_service().create_one_task_type(request, task_type_request)


@router.delete(
    "/{task_type_id}/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK
)
def delete_one(
    task_type_id: int,
    request: Request,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_type_service().delete_one_task_type(task_type_id, request)


@router.put(
    "/{task_type_id}/", response_model=TaskTypeResponse, status_code=HTTPStatus.OK
)
def update_one(
    task_type_id: int,
    request: Request,
    task_type_request: TaskTypeRequest,
    http_basic_credentials: HTTPBasicCredentials = Depends(http_basic_security),
):
    validate_http_basic_credentials(request, http_basic_credentials)
    return get_task_type_service().update_one_task_type(
        task_type_id, request, task_type_request
    )
