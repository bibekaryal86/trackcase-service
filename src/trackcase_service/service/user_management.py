import datetime
import logging
import sys
from http import HTTPStatus
from typing import Type, Union

import bcrypt
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.crud import CrudService, DataKeys
from src.trackcase_service.service import schemas
from src.trackcase_service.utils.commons import (
    decode_email_address,
    encode_auth_credentials,
    get_err_msg,
    raise_http_exception,
)
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)
from src.trackcase_service.utils.email import get_email_service
from src.trackcase_service.utils.logger import Logger

log = Logger(logging.getLogger(__name__))


class AppUserPasswordService:
    def __init__(self, plain_password: str = None, user_name: str = None):
        self.plain_password = plain_password
        self.user_name = user_name

    def login_user(
        self, request: Request, db_session: Session
    ) -> schemas.AppUserLoginResponse:
        crud_service = CrudService(db_session, models.AppUser)
        read_response = crud_service.read(
            filter_config=[
                schemas.FilterConfig(
                    column="email",
                    value=self.user_name.upper(),
                    operation=schemas.FilterOperation.EQUAL_TO,
                )
            ]
        )
        app_user_data_models = read_response.get(DataKeys.data)
        if app_user_data_models and len(app_user_data_models) == 1:
            app_user_data_model: models.AppUser = app_user_data_models[0]

            if app_user_data_model.is_validated:
                is_login_success = self.verify_password(app_user_data_model.password)

                if is_login_success:
                    app_user_data_model.last_login = datetime.datetime.now()
                    crud_service.update(app_user_data_model.id, app_user_data_model)

                    app_user_schema_model = convert_model_to_schema(
                        data_model=app_user_data_model,
                        schema_class=schemas.AppUser,
                    )
                    token_claim = encode_auth_credentials(app_user_schema_model)
                    return schemas.AppUserLoginResponse(
                        token=token_claim, app_user_details=app_user_schema_model
                    )
                else:
                    log.info(
                        "Logging Unsuccessful, password not match for email: [ {} ]".format(  # noqa: E501
                            self.user_name
                        )
                    )
            else:
                log.info(
                    "Logging Unsuccessful, user not validated, please check email: [ {} ]".format(  # noqa: E501
                        self.user_name
                    )
                )
                raise_http_exception(
                    request,
                    HTTPStatus.FORBIDDEN,
                    "Logging Unsuccessful, user not validated, please check email: [ {} ]".format(  # noqa: E501
                        self.user_name
                    ),
                )
        else:
            log.info(
                "Logging Unsuccessful, user not found for email: [ {} ]".format(
                    self.user_name
                )
            )

        raise_http_exception(
            request,
            HTTPStatus.UNAUTHORIZED,
            "Login Unsuccessful! Email and/or password not found in system!! Please try again!!!",  # noqa: E501
        )

    def validate_reset_user(
        self, request: Request, db_session: Session, is_validate: bool = True
    ):
        decoded_email_address = decode_email_address(request, self.user_name)
        crud_service = CrudService(db_session, models.AppUser)

        read_response = crud_service.read(
            filter_config=[
                schemas.FilterConfig(
                    column="email",
                    value=decoded_email_address.upper(),
                    operation=schemas.FilterOperation.EQUAL_TO,
                )
            ]
        )
        app_user_data_models = read_response.get(DataKeys.data)
        if app_user_data_models and len(app_user_data_models) == 1:
            app_user_data_model: models.AppUser = app_user_data_models[0]

            if is_validate:
                app_user_data_model.is_validated = True
                crud_service.update(app_user_data_model.id, app_user_data_model)
            else:
                return app_user_data_model.id
        raise_http_exception(
            request,
            HTTPStatus.FORBIDDEN,
            "Validate Unsuccessful! Email not found in system!! Please try again!!!",
        )

    def hash_password(self) -> str:
        salt = bcrypt.gensalt(rounds=12)
        encoded = self.plain_password.encode("utf-8")
        return bcrypt.hashpw(encoded, salt).decode("utf-8")

    def verify_password(self, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            self.plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )


class AppUserService(CrudService):
    def __init__(self, db_session: Session):
        super(AppUserService, self).__init__(db_session, models.AppUser)

    def create_app_user(
        self, request: Request, request_object: schemas.AppUserRequest
    ) -> schemas.AppUserResponse:
        try:
            if not request_object.password:
                raise_http_exception(
                    request,
                    HTTPStatus.BAD_REQUEST,
                    get_err_msg(
                        "Error Inserting AppUser. Password Missing in Request!!!"
                    ),
                )
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.AppUser
            )
            data_model.password = get_user_password_service(
                request_object.password
            ).hash_password()
            data_model.is_validated = False
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppUser,
            )
            get_email_service().app_user_validation_email(request, data_model.email)
            return schemas.AppUserResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting AppUser. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_app_user(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppUserResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(model_id=metadata.model_id)
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.AppUser,
                    schemas.AppUserResponse,
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppUser,
                    return_type=schemas.AppUserResponse,
                )
            else:
                read_response = self.read()
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppUser,
                    return_type=schemas.AppUserResponse,
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving AppUser. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def check_app_user_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(request_object_id=model_id)
        app_user_response = self.read_app_user(request, request_metadata)
        if not app_user_response or not app_user_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppUser Not Found By Id: {model_id}!!!",
            )

    def update_app_user(
        self, model_id: int, request: Request, request_object: schemas.AppUserRequest
    ) -> schemas.AppUserResponse:
        self.check_app_user_exists(model_id, request)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.AppUser
            )
            if request_object.password:
                data_model.password = get_user_password_service(
                    request_object.password
                ).hash_password()
            data_model = self.update(model_id, data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppUser,
            )
            return schemas.AppUserResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating AppUser By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_app_user(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppUserResponse:
        self.check_app_user_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppUserResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting AppUser By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppRoleService(CrudService):
    def __init__(self, db_session: Session):
        super(AppRoleService, self).__init__(db_session, models.AppRole)

    def create_app_role(
        self, request: Request, request_object: schemas.AppRoleRequest
    ) -> schemas.AppRoleResponse:
        try:
            data_model: models.AppRole = convert_schema_to_model(
                request_object, models.AppRole
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppRole,
            )
            return schemas.AppRoleResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting AppRole. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_app_role(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppRoleResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(model_id=metadata.model_id)
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.AppRole,
                    schemas.AppRoleResponse,
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppRole,
                    return_type=schemas.AppRoleResponse,
                )
            else:
                read_response = self.read()
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppRole,
                    return_type=schemas.AppRoleResponse,
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving AppRole. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def check_app_role_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        app_role_response = self.read_app_role(request, request_metadata)
        if not app_role_response or not app_role_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppRole Not Found By Id: {model_id}!!!",
            )

    def update_app_role(
        self, model_id: int, request: Request, request_object: schemas.AppRoleRequest
    ) -> schemas.AppRoleResponse:
        self.check_app_role_exists(model_id, request)

        try:
            data_model: models.AppRole = convert_schema_to_model(
                request_object, models.AppRole
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppRole,
            )
            return schemas.AppRoleResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating AppRole By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_app_role(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppRoleResponse:
        self.check_app_role_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppRoleResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting AppRole By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppPermissionService(CrudService):
    def __init__(self, db_session: Session):
        super(AppPermissionService, self).__init__(db_session, models.AppPermission)

    def create_app_permission(
        self, request: Request, request_object: schemas.AppPermissionRequest
    ) -> schemas.AppPermissionResponse:
        try:
            data_model: models.AppPermission = convert_schema_to_model(
                request_object, models.AppPermission
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppPermission,
            )
            return schemas.AppPermissionResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting AppPermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_app_permission(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppPermissionResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(model_id=metadata.model_id)
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.AppPermission,
                    schemas.AppPermissionResponse,
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppPermission,
                    return_type=schemas.AppPermissionResponse,
                )
            else:
                read_response = self.read()
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppPermission,
                    return_type=schemas.AppPermissionResponse,
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving AppPermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_app_permission_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        app_permission_response = self.read_app_permission(request, request_metadata)
        if not app_permission_response or not app_permission_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppPermission Not Found By Id: {model_id}!!!",
            )

    def update_app_permission(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppPermissionRequest,
    ) -> schemas.AppPermissionResponse:
        self.check_app_permission_exists(model_id, request)

        try:
            data_model: models.AppPermission = convert_schema_to_model(
                request_object, models.AppPermission
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppPermission,
            )
            return schemas.AppPermissionResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating AppPermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_app_permission(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppPermissionResponse:
        self.check_app_permission_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppPermissionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting AppPermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppUserRoleService(CrudService):
    def __init__(self, db_session: Session):
        super(AppUserRoleService, self).__init__(db_session, models.AppUserRole)

    def create_app_user_role(
        self, request: Request, request_object: schemas.AppUserRoleRequest
    ) -> schemas.AppUserRoleResponse:
        try:
            data_model: models.AppUserRole = convert_schema_to_model(
                request_object, models.AppUserRole
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppUserRole,
            )
            return schemas.AppUserRoleResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting AppUserRole. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_app_user_role(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppUserRoleResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(model_id=metadata.model_id)
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.AppUserRole,
                    schemas.AppUserRoleResponse,
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppUserRole,
                    return_type=schemas.AppUserRoleResponse,
                )
            else:
                read_response = self.read()
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppUserRole,
                    return_type=schemas.AppUserRoleResponse,
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving AppUserRole. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_app_user_role_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        app_user_role_response = self.read_app_user_role(request, request_metadata)
        if not app_user_role_response or not app_user_role_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppUserRole Not Found By Id: {model_id}!!!",
            )

    def update_app_user_role(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppUserRoleRequest,
    ) -> schemas.AppUserRoleResponse:
        self.check_app_user_role_exists(model_id, request)

        try:
            data_model: models.AppUserRole = convert_schema_to_model(
                request_object, models.AppUserRole
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppUserRole,
            )
            return schemas.AppUserRoleResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating AppUserRole By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_app_user_role(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppUserRoleResponse:
        self.check_app_user_role_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppUserRoleResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting AppUserRole By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppRolePermissionService(CrudService):
    def __init__(self, db_session: Session):
        super(AppRolePermissionService, self).__init__(
            db_session, models.AppRolePermission
        )

    def create_app_role_permission(
        self, request: Request, request_object: schemas.AppRolePermissionRequest
    ) -> schemas.AppRolePermissionResponse:
        try:
            data_model: models.AppRolePermission = convert_schema_to_model(
                request_object, models.AppRolePermission
            )
            data_model = self.create(data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppRolePermission,
            )
            return schemas.AppRolePermissionResponse(
                app_role_permissions=[schema_model]
            )
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Inserting AppRolePermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def read_app_role_permission(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppRolePermissionResponse:
        try:
            if metadata is not None and metadata.model_id is not None:
                read_response = self.read(model_id=metadata.model_id)
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.model_id,
                    schemas.AppRolePermission,
                    schemas.AppRolePermissionResponse,
                )
            elif metadata is not None:
                read_response = self.read(
                    sort_config=metadata.sort_config,
                    filter_config=metadata.filter_config,
                    page_number=metadata.page_number,
                    per_page=metadata.per_page,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppRolePermission,
                    return_type=schemas.AppRolePermissionResponse,
                )
            else:
                read_response = self.read()
                return get_user_management_response(
                    read_response,
                    schema_type=schemas.AppRolePermission,
                    return_type=schemas.AppRolePermissionResponse,
                )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    "Error Retrieving AppRolePermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_app_role_permission_exists(self, model_id: int, request: Request):
        request_metadata = schemas.RequestMetadata(model_id=model_id)
        app_role_permission_response = self.read_app_role_permission(
            request, request_metadata
        )
        if not app_role_permission_response or not app_role_permission_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppRolePermission Not Found By Id: {model_id}!!!",
            )

    def update_app_role_permission(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppRolePermissionRequest,
    ) -> schemas.AppRolePermissionResponse:
        self.check_app_role_permission_exists(model_id, request)

        try:
            data_model: models.AppRolePermission = convert_schema_to_model(
                request_object, models.AppRolePermission
            )
            data_model = self.update(model_id, data_model)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppRolePermission,
            )
            return schemas.AppRolePermissionResponse(
                app_role_permissions=[schema_model]
            )
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating AppRolePermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_app_role_permission(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppRolePermissionResponse:
        self.check_app_role_permission_exists(model_id, request)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppRolePermissionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting AppRolePermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


def get_user_management_service(
    service_type: schemas.UserManagementServiceRegistry, db_session: Session
) -> (
    AppUserService
    | AppRoleService
    | AppPermissionService
    | AppUserRoleService
    | AppRolePermissionService
):
    service_registry = {
        schemas.UserManagementServiceRegistry.APP_USER: AppUserService,
        schemas.UserManagementServiceRegistry.APP_ROLE: AppRoleService,
        schemas.UserManagementServiceRegistry.APP_PERMISSION: AppPermissionService,
        schemas.UserManagementServiceRegistry.APP_USER_ROLE: AppUserRoleService,
        schemas.UserManagementServiceRegistry.APP_ROLE_PERMISSION: AppRolePermissionService,  # noqa: E501
    }
    return service_registry.get(service_type)(db_session)


def get_user_password_service(
    plain_password: str = None, user_name: str = None
) -> AppUserPasswordService:
    return AppUserPasswordService(plain_password, user_name)


def get_user_management_response(
    read_response,
    is_single=False,
    request: Request = None,
    model_id: int = None,
    schema_type: Union[
        Type[schemas.AppUser],
        Type[schemas.AppRole],
        Type[schemas.AppPermission],
        Type[schemas.AppUserRole],
        Type[schemas.AppRolePermission],
    ] = None,
    return_type: Union[
        Type[schemas.AppUserResponse],
        Type[schemas.AppRoleResponse],
        Type[schemas.AppPermissionResponse],
        Type[schemas.AppUserRoleResponse],
        Type[schemas.AppRolePermissionResponse],
    ] = None,
) -> Union[
    schemas.AppUserResponse,
    schemas.AppRoleResponse,
    schemas.AppPermissionResponse,
    schemas.AppUserRoleResponse,
    schemas.AppRolePermissionResponse,
]:
    if is_single and not read_response.get(DataKeys.data):
        raise_http_exception(
            request,
            HTTPStatus.NOT_FOUND,
            f"{schema_type.__name__} Not Found By Id: {model_id}!!!",
        )
    data_models = read_response.get(DataKeys.data)
    metadata = read_response.get(DataKeys.metadata)
    schema_models = [
        convert_model_to_schema(data_model=data_model, schema_class=schema_type)
        for data_model in data_models
    ]
    return return_type(
        **{
            "metadata": metadata,
            "data": schema_models,
        }
    )
