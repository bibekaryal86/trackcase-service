from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.ref_types import get_ref_types_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(prefix="/types", tags=["Ref Types"])


@router.get("/ref_types/", summary="Get All Ref Types")
def get_all_ref_types(
    request: Request,
    components: str = Query(default=""),
    db_session: Session = Depends(get_db_session),
):
    ref_types_response_data = schemas.RefTypesResponseData()
    if components:
        component_list = components.split(",")
    else:
        component_list = [
            schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
            schemas.RefTypesServiceRegistry.COLLECTION_METHOD,
            schemas.RefTypesServiceRegistry.CASE_TYPE,
            schemas.RefTypesServiceRegistry.FILING_TYPE,
            schemas.RefTypesServiceRegistry.HEARING_TYPE,
            schemas.RefTypesServiceRegistry.TASK_TYPE,
        ]

    for component in component_list:
        component = component.lower().strip()
        if component == schemas.RefTypesServiceRegistry.COMPONENT_STATUS:
            ref_types_response_data.component_statuses = get_ref_types_service(
                schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
            ).read_component_status(request)
        if component == schemas.RefTypesServiceRegistry.COLLECTION_METHOD:
            ref_types_response_data.collection_methods = get_ref_types_service(
                schemas.RefTypesServiceRegistry.COLLECTION_METHOD, db_session
            ).read_collection_method(request)
        if component == schemas.RefTypesServiceRegistry.CASE_TYPE:
            ref_types_response_data.case_types = get_ref_types_service(
                schemas.RefTypesServiceRegistry.CASE_TYPE, db_session
            ).read_case_type(request)
        if component == schemas.RefTypesServiceRegistry.FILING_TYPE:
            ref_types_response_data.filing_types = get_ref_types_service(
                schemas.RefTypesServiceRegistry.FILING_TYPE, db_session
            ).read_filing_type(request)
        if component == schemas.RefTypesServiceRegistry.HEARING_TYPE:
            ref_types_response_data.hearing_types = get_ref_types_service(
                schemas.RefTypesServiceRegistry.HEARING_TYPE, db_session
            ).read_hearing_type(request)
        if component == schemas.RefTypesServiceRegistry.TASK_TYPE:
            ref_types_response_data.task_types = get_ref_types_service(
                schemas.RefTypesServiceRegistry.TASK_TYPE, db_session
            ).read_task_type(request)
    return schemas.RefTypesResponse(data=ref_types_response_data)


# component_status
@router.post(
    "/component_status/",
    response_model=schemas.ComponentStatusResponse,
    status_code=HTTPStatus.OK,
)
def insert_component_status(
    request: Request,
    component_status_request: schemas.ComponentStatusRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).create_component_status(request, component_status_request)


@router.get(
    "/component_status/",
    response_model=schemas.ComponentStatusResponse,
    status_code=HTTPStatus.OK,
)
def find_component_status(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).read_component_status(request, request_metadata)


@router.put(
    "/component_status/{component_status_id}/",
    response_model=schemas.ComponentStatusResponse,
    status_code=HTTPStatus.OK,
)
def modify_component_status(
    component_status_id: int,
    request: Request,
    component_status_request: schemas.ComponentStatusRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).update_component_status(component_status_id, request, component_status_request)


@router.delete(
    "/component_status/{component_status_id}/{is_hard_delete}/",
    response_model=schemas.ComponentStatusResponse,
    status_code=HTTPStatus.OK,
)
def remove_component_status(
    component_status_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).delete_component_status(component_status_id, is_hard_delete, request)


# collection_method
@router.post(
    "/collection_method/",
    response_model=schemas.CollectionMethodResponse,
    status_code=HTTPStatus.OK,
)
def insert_collection_method(
    request: Request,
    collection_method_request: schemas.CollectionMethodRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).create_collection_method(request, collection_method_request)


@router.get(
    "/collection_method/",
    response_model=schemas.CollectionMethodResponse,
    status_code=HTTPStatus.OK,
)
def find_collection_method(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).read_collection_method(request, request_metadata)


@router.put(
    "/collection_method/{collection_method_id}/",
    response_model=schemas.CollectionMethodResponse,
    status_code=HTTPStatus.OK,
)
def modify_collection_method(
    collection_method_id: int,
    request: Request,
    collection_method_request: schemas.CollectionMethodRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).update_collection_method(collection_method_id, request, collection_method_request)


@router.delete(
    "/collection_method/{collection_method_id}/{is_hard_delete}/",
    response_model=schemas.CollectionMethodResponse,
    status_code=HTTPStatus.OK,
)
def remove_collection_method(
    collection_method_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).delete_collection_method(collection_method_id, is_hard_delete, request)


# case_type
@router.post(
    "/case_type/",
    response_model=schemas.CaseTypeResponse,
    status_code=HTTPStatus.OK,
)
def insert_case_type(
    request: Request,
    case_type_request: schemas.CaseTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).create_case_type(request, case_type_request)


@router.get(
    "/case_type/", response_model=schemas.CaseTypeResponse, status_code=HTTPStatus.OK
)
def find_case_type(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).read_case_type(request, request_metadata)


@router.put(
    "/case_type/{case_type_id}/",
    response_model=schemas.CaseTypeResponse,
    status_code=HTTPStatus.OK,
)
def modify_case_type(
    case_type_id: int,
    request: Request,
    case_type_request: schemas.CaseTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).update_case_type(case_type_id, request, case_type_request)


@router.delete(
    "/case_type/{case_type_id}/{is_hard_delete}/",
    response_model=schemas.CaseTypeResponse,
    status_code=HTTPStatus.OK,
)
def remove_case_type(
    case_type_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).delete_case_type(case_type_id, is_hard_delete, request)


# filing_type
@router.post(
    "/filing_type/",
    response_model=schemas.FilingTypeResponse,
    status_code=HTTPStatus.OK,
)
def insert_filing_type(
    request: Request,
    filing_type_request: schemas.FilingTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).create_filing_type(request, filing_type_request)


@router.get(
    "/filing_type/",
    response_model=schemas.FilingTypeResponse,
    status_code=HTTPStatus.OK,
)
def find_filing_type(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).read_filing_type(request, request_metadata)


@router.put(
    "/filing_type/{filing_type_id}/",
    response_model=schemas.FilingTypeResponse,
    status_code=HTTPStatus.OK,
)
def modify_filing_type(
    filing_type_id: int,
    request: Request,
    filing_type_request: schemas.FilingTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).update_filing_type(filing_type_id, request, filing_type_request)


@router.delete(
    "/filing_type/{filing_type_id}/{is_hard_delete}/",
    response_model=schemas.FilingTypeResponse,
    status_code=HTTPStatus.OK,
)
def remove_filing_type(
    filing_type_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).delete_filing_type(filing_type_id, is_hard_delete, request)


# hearing_type
@router.post(
    "/hearing_type/",
    response_model=schemas.HearingTypeResponse,
    status_code=HTTPStatus.OK,
)
def insert_hearing_type(
    request: Request,
    hearing_type_request: schemas.HearingTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).create_hearing_type(request, hearing_type_request)


@router.get(
    "/hearing_type/",
    response_model=schemas.HearingTypeResponse,
    status_code=HTTPStatus.OK,
)
def find_hearing_type(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).read_hearing_type(request, request_metadata)


@router.put(
    "/hearing_type/{hearing_type_id}/",
    response_model=schemas.HearingTypeResponse,
    status_code=HTTPStatus.OK,
)
def modify_hearing_type(
    hearing_type_id: int,
    request: Request,
    hearing_type_request: schemas.HearingTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).update_hearing_type(hearing_type_id, request, hearing_type_request)


@router.delete(
    "/hearing_type/{hearing_type_id}/{is_hard_delete}/",
    response_model=schemas.HearingTypeResponse,
    status_code=HTTPStatus.OK,
)
def remove_hearing_type(
    hearing_type_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).delete_hearing_type(hearing_type_id, is_hard_delete, request)


# task_type
@router.post(
    "/task_type/",
    response_model=schemas.TaskTypeResponse,
    status_code=HTTPStatus.OK,
)
def insert_task_type(
    request: Request,
    task_type_request: schemas.TaskTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).create_task_type(request, task_type_request)


@router.get(
    "/task_type/", response_model=schemas.TaskTypeResponse, status_code=HTTPStatus.OK
)
def find_task_type(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).read_task_type(request, request_metadata)


@router.put(
    "/task_type/{task_type_id}/",
    response_model=schemas.TaskTypeResponse,
    status_code=HTTPStatus.OK,
)
def modify_task_type(
    task_type_id: int,
    request: Request,
    task_type_request: schemas.TaskTypeRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).update_task_type(task_type_id, request, task_type_request)


@router.delete(
    "/task_type/{task_type_id}/{is_hard_delete}/",
    response_model=schemas.TaskTypeResponse,
    status_code=HTTPStatus.OK,
)
def remove_task_type(
    task_type_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_ref_types_service(
        schemas.RefTypesServiceRegistry.COMPONENT_STATUS, db_session
    ).delete_task_type(task_type_id, is_hard_delete, request)
