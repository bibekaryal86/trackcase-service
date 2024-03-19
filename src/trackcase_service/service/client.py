import sys
from http import HTTPStatus

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.trackcase_service.db import models
from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.service import schemas
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.ref_types import get_ref_types_service
from src.trackcase_service.utils.commons import (
    check_active_component_status,
    check_permissions,
    get_err_msg,
    get_read_response_data_metadata,
    raise_http_exception,
)
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)


class ClientService(CrudService):
    def __init__(self, db_session: Session):
        super(ClientService, self).__init__(db_session, models.Client)

    @check_permissions("clients_create")
    def create_client(
        self, request: Request, request_object: schemas.ClientRequest
    ) -> schemas.ClientResponse:
        try:
            data_model: models.Client = convert_schema_to_model(
                request_object, models.Client
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryClient
            ).add_to_history(
                request,
                request_object,
                "client_id",
                data_model.id,
                "Client",
                "HistoryClient",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Client,
                exclusions=[
                    "court_cases",
                    "history_clients",
                    "history_court_cases",
                ],
            )
            return schemas.ClientResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting Client. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("clients_read")
    def read_client(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.ClientResponse:
        try:
            if request_metadata:
                if request_metadata.schema_model_id:
                    read_response = self.read(
                        model_id=request_metadata.schema_model_id,
                        is_include_soft_deleted=request_metadata.is_include_deleted,
                    )
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
                    if not response_data:
                        raise_http_exception(
                            request,
                            HTTPStatus.NOT_FOUND,
                            f"Client Not Found By Id: {request_metadata.schema_model_id}!!!",
                        )
                else:
                    read_response = self.read(
                        sort_config=request_metadata.sort_config,
                        filter_config=request_metadata.filter_config,
                        page_number=request_metadata.page_number,
                        per_page=request_metadata.per_page,
                        is_include_soft_deleted=request_metadata.is_include_deleted
                        is True,
                    )
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
            else:
                request_metadata = schemas.RequestMetadata()
                read_response = self.read()
                response_data, response_metadata = get_read_response_data_metadata(
                    read_response
                )

            schema_models = [
                convert_model_to_schema(
                    data_model=data_model,
                    schema_class=schemas.Client,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "court_cases",
                        "history_clients",
                        "history_court_cases",
                    ],
                    extra_to_include=["court_cases"],
                    history_to_include=["history_clients"],
                )
                for data_model in response_data
            ]
            return schemas.ClientResponse(
                data=schema_models, metadata=response_metadata
            )
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving Client. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("clients_update")
    def update_client(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.ClientRequest,
        is_restore: bool = False,
    ) -> schemas.ClientResponse:
        client_old = self.check_client_exists(model_id, request, is_restore)
        self.check_client_dependents_statuses(
            request, request_object.component_status_id, client_old
        )

        try:
            data_model: models.Client = convert_schema_to_model(
                request_object, models.Client
            )
            data_model = self.update(model_id, data_model, is_restore)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryClient
            ).add_to_history(
                request,
                request_object,
                "client_id",
                data_model.id,
                "Client",
                "HistoryClient",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Client,
                exclusions=[
                    "court_cases",
                    "history_clients",
                    "history_court_cases",
                ],
            )
            return schemas.ClientResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating Client By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("clients_delete")
    def delete_client(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.ClientResponse:
        client_old = self.check_client_exists(model_id, request, is_hard_delete)
        if client_old.court_cases:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete Client {model_id}, There are Linked Court Cases!",  # noqa: E501
            )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryClient
            ).delete_history_before_delete_object(
                models.HistoryClient.__tablename__,
                "client_id",
                model_id,
                "Client",
                "HistoryClient",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryClient
            ).add_to_history(
                request,
                client_old,
                "client_id",
                model_id,
                "Client",
                "HistoryClient",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.ClientResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting Client By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_client_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ) -> schemas.Client:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id,
            is_include_extra=True,
            is_include_deleted=is_include_deleted,
        )
        client_response = self.read_client(request, request_metadata)
        if not client_response or not client_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Client Not Found By Id: {model_id}!!!",
            )
        return client_response.data[0]

    def check_client_dependents_statuses(
        self,
        request: Request,
        status_new: int,
        client_old: schemas.Client,
    ):
        if client_old.court_cases:
            status_old = client_old.component_status_id
            ref_types_service = get_ref_types_service(
                service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
                db_session=self.db_session,
            )
            client_active_statuses = ref_types_service.get_component_status(
                request,
                schemas.ComponentStatusNames.CLIENT,
                schemas.ComponentStatusTypes.ACTIVE,
            )
            active_status_ids_client = [
                component_status.id for component_status in client_active_statuses
            ]

            if status_new != status_old and status_new not in active_status_ids_client:
                court_case_active_statuses = ref_types_service.get_component_status(
                    request,
                    schemas.ComponentStatusNames.COURT_CASE,
                    schemas.ComponentStatusTypes.ACTIVE,
                )
                active_status_ids_court_case = [
                    component_status.id
                    for component_status in court_case_active_statuses
                ]
                if check_active_component_status(
                    client_old.court_cases, active_status_ids_court_case
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update Client {client_old.id} Status to {status_new}, There are Active Court Cases!",  # noqa: E501
                    )


def get_client_service(db_session: Session) -> ClientService:
    return ClientService(db_session)
