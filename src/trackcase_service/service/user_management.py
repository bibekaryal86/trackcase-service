import datetime
import logging
import sys
from http import HTTPStatus
from typing import Type, Union

import bcrypt
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.crud import CrudService, CrudServiceRaw, DataKeys
from src.trackcase_service.service import schemas
from src.trackcase_service.utils.cache import (
    get_app_permissions_cache,
    get_app_roles_cache,
    set_app_permissions_cache,
    set_app_roles_cache,
)
from src.trackcase_service.utils.commons import (
    check_permissions,
    decode_email_address,
    encode_auth_credentials,
    get_err_msg,
    get_filter_config_raw,
    get_sort_config_raw,
    raise_http_exception,
)
from src.trackcase_service.utils.constants import (
    GUEST_USER_ROLE_ID,
    STANDARD_USER_ROLE_ID,
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
        app_user_data_models = []
        try:
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
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Logging in AppUser. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

        if app_user_data_models and len(app_user_data_models) == 1:
            app_user_data_model: models.AppUser = app_user_data_models[0]

            if app_user_data_model.is_validated:
                is_login_success = self.verify_password(app_user_data_model.password)

                if is_login_success:
                    try:
                        # this should not prevent users from logging in
                        app_user_data_model.last_login = datetime.datetime.now()
                        crud_service.update(app_user_data_model.id, app_user_data_model)
                    except Exception as ex:
                        log.error(
                            "Logging successful, but last_login not updated for email: [ {} ]".format(  # noqa: E501
                                self.user_name
                            ),
                            extra=ex,
                            exc_info=sys.exc_info(),
                        )

                    app_user_schema_model = convert_model_to_schema(
                        data_model=app_user_data_model,
                        schema_class=schemas.AppUser,
                    )

                    role_ids = [
                        app_role.id for app_role in app_user_schema_model.app_roles
                    ]
                    app_role_models = (
                        CrudService(db_session, models.AppRole)
                        .read(model_ids=role_ids)
                        .get(DataKeys.data)
                    )
                    app_role_schemas = [
                        convert_model_to_schema(
                            data_model=app_role_model,
                            schema_class=schemas.AppRole,
                            exclusions=["app_users"],
                        )
                        for app_role_model in app_role_models
                    ]
                    app_user_schema_model.app_roles = app_role_schemas
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
        try:
            crud_service = CrudService(db_session, models.AppUser)
            app_user_data_models = self._read_and_respond(request, crud_service)

            if app_user_data_models and len(app_user_data_models) == 1:
                app_user_data_model: models.AppUser = app_user_data_models[0]

                if is_validate:
                    app_user_data_model.is_validated = True
                    crud_service.update(app_user_data_model.id, app_user_data_model)
                else:
                    return app_user_data_model.email
            else:
                raise_http_exception(
                    request,
                    HTTPStatus.FORBIDDEN,
                    "Validate Unsuccessful! User not found in system!! Please try again!!!",  # noqa: E501
                )
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.FORBIDDEN,
                f"Validate Unsuccessful. Please try again! {str(ex)} ",
                sys.exc_info(),
            )

    def _read_and_respond(
        self,
        request: Request,
        crud_service: CrudService,
        is_plain_username: bool = False,
    ):
        if is_plain_username:
            decoded_email_address = self.user_name
        else:
            decoded_email_address = decode_email_address(request, self.user_name)
        read_response = crud_service.read(
            filter_config=[
                schemas.FilterConfig(
                    column="email",
                    value=decoded_email_address.upper(),
                    operation=schemas.FilterOperation.EQUAL_TO,
                )
            ]
        )
        return read_response.get(DataKeys.data)

    def reset_user_password(self, request: Request, db_session: Session):
        try:
            crud_service = CrudService(db_session, models.AppUser)
            app_user_data_models = self._read_and_respond(request, crud_service, True)

            if app_user_data_models and len(app_user_data_models) == 1:
                app_user_data_model: models.AppUser = app_user_data_models[0]
                app_user_data_model.password = self.hash_password()
                crud_service.update(app_user_data_model.id, app_user_data_model)
            else:
                raise_http_exception(
                    request,
                    HTTPStatus.FORBIDDEN,
                    "Reset Unsuccessful! User not found in system!! Please try again!!!",  # noqa: E501
                )
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Reset Unsuccessful. Please try again! {str(ex)} ",
                sys.exc_info(),
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

            app_role_id_to_assign = (
                GUEST_USER_ROLE_ID
                if request_object.is_guest_user
                else STANDARD_USER_ROLE_ID
            )
            get_user_management_service(
                schemas.UserManagementServiceRegistry.APP_USER_ROLE, self.db_session
            ).create_app_user_role(
                request,
                schemas.AppUserRoleRequest(
                    app_user_id=data_model.id, app_role_id=app_role_id_to_assign
                ),
            )
            get_email_service().app_user_validation_email(request, data_model.email)
            return schemas.AppUserResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting AppUser. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_USERS_READ")
    def read_app_user(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppUserResponse:
        try:
            if metadata is not None and metadata.schema_model_id is not None:
                read_response = self.read(
                    model_id=metadata.schema_model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.schema_model_id,
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving AppUser. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def check_app_user_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            request_object_id=model_id, is_include_deleted=is_include_deleted
        )
        app_user_response = self.read_app_user(request, request_metadata)
        if not app_user_response or not app_user_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppUser Not Found By Id: {model_id}!!!",
            )

    @check_permissions("APP_USERS_UPDATE")
    def update_app_user(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppUserRequest,
        is_restore: bool = False,
    ) -> schemas.AppUserResponse:
        self.check_app_user_exists(model_id, request, is_restore)

        try:
            data_model: models.AppUser = convert_schema_to_model(
                request_object, models.AppUser
            )
            if request_object.password:
                data_model.password = get_user_password_service(
                    request_object.password
                ).hash_password()
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppUser,
            )
            return schemas.AppUserResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating AppUser By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_USERS_DELETE")
    def delete_app_user(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppUserResponse:
        self.check_app_user_exists(model_id, request, is_hard_delete)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppUserResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting AppUser By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppRoleService(CrudService):
    def __init__(self, db_session: Session):
        super(AppRoleService, self).__init__(db_session, models.AppRole)

    @check_permissions("APP_ROLES_CREATE")
    def create_app_role(
        self, request: Request, request_object: schemas.AppRoleRequest
    ) -> schemas.AppRoleResponse:
        set_app_roles_cache([])
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting AppRole. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_ROLES_READ")
    def read_app_role(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppRoleResponse:
        try:
            if metadata is not None and metadata.schema_model_id is not None:
                read_response = self.read(
                    model_id=metadata.schema_model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.schema_model_id,
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving AppRole. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def get_app_role(
        self,
        request: Request,
    ) -> list[schemas.AppRole]:
        app_roles = get_app_roles_cache()
        if not app_roles:
            app_roles = self.read_app_role(request).data or []
            set_app_roles_cache(app_roles)
        return app_roles

    def check_app_role_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        app_role_response = self.read_app_role(request, request_metadata)
        if not app_role_response or not app_role_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppRole Not Found By Id: {model_id}!!!",
            )

    @check_permissions("APP_ROLES_UPDATE")
    def update_app_role(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppRoleRequest,
        is_restore: bool = False,
    ) -> schemas.AppRoleResponse:
        set_app_roles_cache([])
        self.check_app_role_exists(model_id, request, is_restore)

        try:
            data_model: models.AppRole = convert_schema_to_model(
                request_object, models.AppRole
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppRole,
            )
            return schemas.AppRoleResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating AppRole By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_ROLES_DELETE")
    def delete_app_role(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppRoleResponse:
        set_app_roles_cache([])
        self.check_app_role_exists(model_id, request, is_hard_delete)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppRoleResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting AppRole By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppPermissionService(CrudService):
    def __init__(self, db_session: Session):
        super(AppPermissionService, self).__init__(db_session, models.AppPermission)

    @check_permissions("APP_PERMISSIONS_CREATE")
    def create_app_permission(
        self, request: Request, request_object: schemas.AppPermissionRequest
    ) -> schemas.AppPermissionResponse:
        set_app_permissions_cache([])
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting AppPermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_PERMISSIONS_READ")
    def read_app_permission(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppPermissionResponse:
        try:
            if metadata is not None and metadata.schema_model_id is not None:
                read_response = self.read(
                    model_id=metadata.schema_model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.schema_model_id,
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving AppPermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def get_app_permission(
        self,
        request: Request,
    ) -> list[schemas.AppPermission]:
        app_permissions = get_app_permissions_cache()
        if not app_permissions:
            app_permissions = self.read_app_permission(request).data or []
            set_app_permissions_cache(app_permissions)
        return app_permissions

    def check_app_permission_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        app_permission_response = self.read_app_permission(request, request_metadata)
        if not app_permission_response or not app_permission_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppPermission Not Found By Id: {model_id}!!!",
            )

    @check_permissions("APP_PERMISSIONS_UPDATE")
    def update_app_permission(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppPermissionRequest,
        is_restore: bool = False,
    ) -> schemas.AppPermissionResponse:
        self.check_app_permission_exists(model_id, request, is_restore)

        try:
            data_model: models.AppPermission = convert_schema_to_model(
                request_object, models.AppPermission
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppPermission,
            )
            return schemas.AppPermissionResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating AppPermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_PERMISSIONS_DELETE")
    def delete_app_permission(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppPermissionResponse:
        self.check_app_permission_exists(model_id, request, is_hard_delete)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppPermissionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting AppPermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppUserRoleService(CrudService):
    def __init__(self, db_session: Session):
        super(AppUserRoleService, self).__init__(db_session, models.AppUserRole)

    @check_permissions("APP_USERS_ROLES_CREATE")
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting AppUserRole. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_USERS_ROLES_READ")
    def read_app_user_role(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppUserRoleResponse:
        try:
            if metadata is not None and metadata.schema_model_id is not None:
                read_response = self.read(
                    model_id=metadata.schema_model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.schema_model_id,
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving AppUserRole. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_app_user_role_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        app_user_role_response = self.read_app_user_role(request, request_metadata)
        if not app_user_role_response or not app_user_role_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppUserRole Not Found By Id: {model_id}!!!",
            )

    @check_permissions("APP_USERS_ROLES_UPDATE")
    def update_app_user_role(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppUserRoleRequest,
        is_restore: bool = False,
    ) -> schemas.AppUserRoleResponse:
        self.check_app_user_role_exists(model_id, request, is_restore)

        try:
            data_model: models.AppUserRole = convert_schema_to_model(
                request_object, models.AppUserRole
            )
            data_model = self.update(model_id, data_model, is_restore)
            schema_model = convert_model_to_schema(
                data_model=data_model,
                schema_class=schemas.AppUserRole,
            )
            return schemas.AppUserRoleResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating AppUserRole By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_USERS_ROLES_DELETE")
    def delete_app_user_role(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppUserRoleResponse:
        self.check_app_user_role_exists(model_id, request, is_hard_delete)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppUserRoleResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
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

    @check_permissions("APP_ROLES_PERMISSIONS_CREATE")
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Inserting AppRolePermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_ROLES_PERMISSIONS_READ")
    def read_app_role_permission(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppRolePermissionResponse:
        try:
            if metadata is not None and metadata.schema_model_id is not None:
                read_response = self.read(
                    model_id=metadata.schema_model_id,
                    is_include_soft_deleted=metadata.is_include_deleted,
                )
                return get_user_management_response(
                    read_response,
                    True,
                    request,
                    metadata.schema_model_id,
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving AppRolePermission. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    def check_app_role_permission_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ):
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_deleted=is_include_deleted
        )
        app_role_permission_response = self.read_app_role_permission(
            request, request_metadata
        )
        if not app_role_permission_response or not app_role_permission_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"AppRolePermission Not Found By Id: {model_id}!!!",
            )

    @check_permissions("APP_ROLES_PERMISSIONS_UPDATE")
    def update_app_role_permission(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.AppRolePermissionRequest,
        is_restore: bool = False,
    ) -> schemas.AppRolePermissionResponse:
        self.check_app_role_permission_exists(model_id, request, is_restore)

        try:
            data_model: models.AppRolePermission = convert_schema_to_model(
                request_object, models.AppRolePermission
            )
            data_model = self.update(model_id, data_model, is_restore)
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
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating AppRolePermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_ROLES_PERMISSIONS_DELETE")
    def delete_app_role_permission(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.AppRolePermissionResponse:
        self.check_app_role_permission_exists(model_id, request, is_hard_delete)

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.AppRolePermissionResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting AppRolePermission By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


class AppUserRolePermissionService(CrudServiceRaw):
    def __init__(self, db_session: Session):
        super(AppUserRolePermissionService, self).__init__(db_session)

    @check_permissions("APP_USERS_ROLES_READ")
    def read_app_user_role_raw(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppUserRoleResponse:
        page_number = 1
        per_page = 100
        is_where_used = False
        try:
            sql_query = (
                "SELECT app_user_role.id, app_user_role.created, app_user_role.modified, "  # noqa: E501
                "app_user_role.is_deleted, app_user_role.deleted_date, "
                "app_user_role.app_user_id, app_user_role.app_role_id, "
                "app_user.email, app_user.full_name, app_role.name as role_name "
                "FROM app_user_role "
                "INNER JOIN app_user ON app_user_role.app_user_id = app_user.id "
                "INNER JOIN app_role on app_user_role.app_role_id = app_role.id"
            )
            if metadata is not None:
                if metadata.schema_model_id is not None:
                    is_where_used = True
                    sql_query += f" WHERE app_user_role.id = {metadata.schema_model_id}"
                elif metadata.filter_config:
                    filter_config = get_filter_config_raw(metadata.filter_config)
                    if filter_config:
                        is_where_used = True
                        sql_query += f" WHERE {filter_config}"

                if metadata.is_include_deleted:
                    pass
                else:
                    if is_where_used:
                        sql_query += " AND app_user_role.is_deleted = false"
                    else:
                        sql_query += " WHERE app_user_role.is_deleted = false"

                sort_config = get_sort_config_raw(metadata.sort_config)
                if sort_config:
                    sql_query += sort_config

            read_response = self.read(
                schemas.AppUserRole, sql_query, page_number, per_page
            )
            return schemas.AppUserRoleResponse(
                **{
                    "data": read_response.get(DataKeys.data),
                    "metadata": read_response.get(DataKeys.metadata),
                }
            )
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving AppUserRole. Please Try Again!!!", str(ex)
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("APP_ROLES_PERMISSIONS_READ")
    def read_app_role_permission_raw(
        self, request: Request, metadata: schemas.RequestMetadata = None
    ) -> schemas.AppRolePermissionResponse:
        page_number = 1
        per_page = 100
        is_where_used = False
        try:
            sql_query = (
                "SELECT app_role_permission.id, app_role_permission.created, app_role_permission.modified, "  # noqa: E501
                "app_role_permission.is_deleted, app_role_permission.deleted_date, "
                "app_role_permission.app_role_id, app_role_permission.app_permission_id, "  # noqa: E501
                "app_role.name as role_name, app_permission.name as permission_name "
                "FROM app_role_permission "
                "INNER JOIN app_role ON app_role_permission.app_role_id = app_role.id "
                "INNER JOIN app_permission on app_role_permission.app_permission_id = app_permission.id"  # noqa: E501
            )
            if metadata is not None:
                if metadata.schema_model_id is not None:
                    is_where_used = True
                    sql_query += (
                        f" WHERE app_role_permission.id = {metadata.schema_model_id}"
                    )
                elif metadata.filter_config:
                    filter_config = get_filter_config_raw(metadata.filter_config)
                    if filter_config:
                        is_where_used = True
                        sql_query += f" WHERE {filter_config}"

                if metadata.is_include_deleted:
                    pass
                else:
                    if is_where_used:
                        sql_query += " AND app_role_permission.is_deleted = false"
                    else:
                        sql_query += " WHERE app_role_permission.is_deleted = false"

                sort_config = get_sort_config_raw(metadata.sort_config)
                if sort_config:
                    sql_query += sort_config

            read_response = self.read(
                schemas.AppRolePermission, sql_query, page_number, per_page
            )
            return schemas.AppRolePermissionResponse(
                **{
                    "data": read_response.get(DataKeys.data),
                    "metadata": read_response.get(DataKeys.metadata),
                }
            )
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    "Error Retrieving AppUserRole. Please Try Again!!!", str(ex)
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
    | AppUserRolePermissionService
):
    service_registry = {
        schemas.UserManagementServiceRegistry.APP_USER: AppUserService,
        schemas.UserManagementServiceRegistry.APP_ROLE: AppRoleService,
        schemas.UserManagementServiceRegistry.APP_PERMISSION: AppPermissionService,
        schemas.UserManagementServiceRegistry.APP_USER_ROLE: AppUserRoleService,
        schemas.UserManagementServiceRegistry.APP_ROLE_PERMISSION: AppRolePermissionService,  # noqa: E501
        schemas.UserManagementServiceRegistry.APP_USER_ROLE_PERMISSION: AppUserRolePermissionService,  # noqa: E501
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
