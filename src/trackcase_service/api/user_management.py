from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.session import get_db_session
from src.trackcase_service.service import schemas
from src.trackcase_service.service.user_management import get_user_management_service
from src.trackcase_service.utils.commons import parse_request_metadata

router = APIRouter(
    prefix="/trackcase-service/users",
    tags=["User Management"],
)


# app users
@router.post(
    "/app_users/", response_model=schemas.AppUserResponse, status_code=HTTPStatus.OK
)
def insert_app_user(
    request: Request,
    app_user_request: schemas.AppUserRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER, db_session
    ).create_app_user(request, app_user_request)


@router.get(
    "/app_users/", response_model=schemas.AppUserResponse, status_code=HTTPStatus.OK
)
def find_app_users(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER, db_session
    ).read_app_user(request, request_metadata)


@router.put(
    "/app_users/{app_user_id}/",
    response_model=schemas.AppUserResponse,
    status_code=HTTPStatus.OK,
)
def modify_app_user(
    app_user_id: int,
    request: Request,
    app_user_request: schemas.AppUserRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER, db_session
    ).update_app_user(app_user_id, request, app_user_request)


@router.delete(
    "/app_users/{app_user_id}/{is_hard_delete}/",
    response_model=schemas.AppUserResponse,
    status_code=HTTPStatus.OK,
)
def remove_app_user(
    app_user_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER, db_session
    ).delete_app_user(app_user_id, is_hard_delete, request)


# app roles
@router.post(
    "/app_roles/", response_model=schemas.AppRoleResponse, status_code=HTTPStatus.OK
)
def insert_app_role(
    request: Request,
    app_role_request: schemas.AppRoleRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE, db_session
    ).create_app_role(request, app_role_request)


@router.get(
    "/app_roles/", response_model=schemas.AppRoleResponse, status_code=HTTPStatus.OK
)
def find_app_roles(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE, db_session
    ).read_app_role(request, request_metadata)


@router.put(
    "/app_roles/{app_role_id}/",
    response_model=schemas.AppRoleResponse,
    status_code=HTTPStatus.OK,
)
def modify_app_role(
    app_role_id: int,
    request: Request,
    app_role_request: schemas.AppRoleRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE, db_session
    ).update_app_role(app_role_id, request, app_role_request)


@router.delete(
    "/app_roles/{app_role_id}/{is_hard_delete}/",
    response_model=schemas.AppRoleResponse,
    status_code=HTTPStatus.OK,
)
def remove_app_role(
    app_role_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE, db_session
    ).delete_app_role(app_role_id, is_hard_delete, request)


# app permissions
@router.post(
    "/app_permissions/",
    response_model=schemas.AppPermissionResponse,
    status_code=HTTPStatus.OK,
)
def insert_app_permission(
    request: Request,
    app_permission_request: schemas.AppPermissionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_PERMISSION, db_session
    ).create_app_permission(request, app_permission_request)


@router.get(
    "/app_permissions/",
    response_model=schemas.AppPermissionResponse,
    status_code=HTTPStatus.OK,
)
def find_app_permissions(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_PERMISSION, db_session
    ).read_app_permission(request, request_metadata)


@router.put(
    "/app_permissions/{app_permission_id}/",
    response_model=schemas.AppPermissionResponse,
    status_code=HTTPStatus.OK,
)
def modify_app_permission(
    app_permission_id: int,
    request: Request,
    app_permission_request: schemas.AppPermissionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_PERMISSION, db_session
    ).update_app_permission(app_permission_id, request, app_permission_request)


@router.delete(
    "/app_permissions/{app_permission_id}/{is_hard_delete}/",
    response_model=schemas.AppPermissionResponse,
    status_code=HTTPStatus.OK,
)
def remove_app_permission(
    app_permission_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_PERMISSION, db_session
    ).delete_app_permission(app_permission_id, is_hard_delete, request)


# app user role
@router.post(
    "/app_user_roles/",
    response_model=schemas.AppUserRoleResponse,
    status_code=HTTPStatus.OK,
)
def insert_app_user_role(
    request: Request,
    app_user_role_request: schemas.AppUserRoleRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER_ROLE, db_session
    ).create_app_user_role(request, app_user_role_request)


@router.get(
    "/app_user_roles/",
    response_model=schemas.AppUserRoleResponse,
    status_code=HTTPStatus.OK,
)
def find_app_user_roles(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER_ROLE, db_session
    ).read_app_user_role(request, request_metadata)


@router.put(
    "/app_user_roles/{app_user_role_id}/",
    response_model=schemas.AppUserRoleResponse,
    status_code=HTTPStatus.OK,
)
def modify_app_user_role(
    app_user_role_id: int,
    request: Request,
    app_user_role_request: schemas.AppUserRoleRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER_ROLE, db_session
    ).update_app_user_role(app_user_role_id, request, app_user_role_request)


@router.delete(
    "/app_user_roles/{app_user_role_id}/{is_hard_delete}/",
    response_model=schemas.AppUserRoleResponse,
    status_code=HTTPStatus.OK,
)
def remove_app_user_role(
    app_user_role_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_USER_ROLE, db_session
    ).delete_app_user_role(app_user_role_id, is_hard_delete, request)


# app role permission
@router.post(
    "/app_role_permissions/",
    response_model=schemas.AppRolePermissionResponse,
    status_code=HTTPStatus.OK,
)
def insert_app_role_permission(
    request: Request,
    app_role_permission_request: schemas.AppRolePermissionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE_PERMISSION, db_session
    ).create_app_role_permission(request, app_role_permission_request)


@router.get(
    "/app_role_permissions/",
    response_model=schemas.AppRolePermissionResponse,
    status_code=HTTPStatus.OK,
)
def find_app_role_permissions(
    request: Request,
    request_metadata: schemas.RequestMetadata = Depends(parse_request_metadata),
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE_PERMISSION, db_session
    ).read_app_role_permission(request, request_metadata)


@router.put(
    "/app_role_permissions/{app_role_permission_id}/",
    response_model=schemas.AppRolePermissionResponse,
    status_code=HTTPStatus.OK,
)
def modify_app_role_permission(
    app_role_permission_id: int,
    request: Request,
    app_role_permission_request: schemas.AppRolePermissionRequest,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE_PERMISSION, db_session
    ).update_app_role_permission(
        app_role_permission_id, request, app_role_permission_request
    )


@router.delete(
    "/app_role_permissions/{app_role_permission_id}/{is_hard_delete}/",
    response_model=schemas.AppRolePermissionResponse,
    status_code=HTTPStatus.OK,
)
def remove_app_role_permission(
    app_role_permission_id: int,
    request: Request,
    is_hard_delete: bool = False,
    db_session: Session = Depends(get_db_session),
):
    return get_user_management_service(
        schemas.UserManagementServiceRegistry.APP_ROLE_PERMISSION, db_session
    ).delete_app_role_permission(app_role_permission_id, is_hard_delete, request)
