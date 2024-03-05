import sys
from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Client as ClientModel
from src.trackcase_service.db.models import HistoryClient as HistoryClientModel
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.schemas import Client as ClientSchema
from src.trackcase_service.service.schemas import ClientRequest, ClientResponse
from src.trackcase_service.utils.commons import (
    check_active_court_cases,
    get_err_msg,
    raise_http_exception,
)
from src.trackcase_service.utils.constants import get_statuses
from src.trackcase_service.utils.convert import (
    convert_client_model_to_schema,
    convert_schema_to_model,
)


class ClientService(CrudService):
    def __init__(self, db_session: Session):
        super(ClientService, self).__init__(db_session, ClientModel)

    def create_one_client(
        self, request: Request, request_object: ClientRequest
    ) -> ClientResponse:
        try:
            data_model: ClientModel = convert_schema_to_model(
                request_object, ClientModel
            )
            data_model = super().create(data_model)
            _handle_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_client_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting Client. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_one_client(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> ClientResponse:
        try:
            data_model: ClientModel = super().read_one(model_id)
            if data_model:
                schema_model: ClientSchema = convert_client_model_to_schema(
                    data_model,
                    is_include_extra,
                    is_include_history,
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving Client By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def read_all_clients(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> ClientResponse:
        try:
            sort_config = {"name": "asc"}
            data_models: List[ClientModel] = super().read_all(sort_config)
            schema_models: List[ClientSchema] = [
                convert_client_model_to_schema(
                    data_model,
                    is_include_extra,
                    is_include_history,
                )
                for data_model in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving Clients. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def update_one_client(
        self, model_id: int, request: Request, request_object: ClientRequest
    ) -> ClientResponse:
        client_response = self.read_one_client(model_id, request, is_include_extra=True)

        if not (client_response and client_response.clients):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Client Not Found By Id: {model_id}!!!",
            )

        _check_dependents_statuses(
            request, request_object.status, client_response.clients[0]
        )

        try:
            data_model: ClientModel = convert_schema_to_model(
                request_object, ClientModel
            )
            data_model = super().update(model_id, data_model)
            _handle_history(self.db_session, request, model_id, request_object)
            schema_model = convert_client_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating Client By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_one_client(self, model_id: int, request: Request) -> ClientResponse:
        client_response = self.read_one_client(model_id, request, is_include_extra=True)

        if not (client_response and client_response.clients):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Client Not Found By Id: {model_id}!!!",
            )

        _check_dependents(request, client_response.clients[0])
        _handle_history(self.db_session, request, model_id, is_delete=True)

        try:
            super().delete(model_id)
            return ClientResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Client By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )


def get_client_service(db_session: Session) -> ClientService:
    return ClientService(db_session)


def get_response_single(single: ClientSchema) -> ClientResponse:
    return ClientResponse(clients=[single])


def get_response_multiple(multiple: list[ClientSchema]) -> ClientResponse:
    return ClientResponse(clients=multiple)


def _check_dependents_statuses(
    request: Request,
    status_new: str,
    client_old: ClientSchema,
):
    status_old = client_old.status
    inactive_statuses = get_statuses().get("client").get("inactive")
    if status_new != status_old and status_new in inactive_statuses:
        if check_active_court_cases(client_old.court_cases):
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Update Client {client_old.id} Status to {status_new}, There are Active Court Cases!",  # noqa: E501
            )


def _check_dependents(request: Request, client: ClientSchema):
    if client.court_cases:
        raise_http_exception(
            request,
            HTTPStatus.UNPROCESSABLE_ENTITY,
            f"Cannot Delete Client {client.id}, There are Linked Court Cases!",
        )


def _handle_history(
    db_session: Session,
    request: Request,
    client_id: int,
    request_object: ClientRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryClientModel)
    if is_delete:
        history_service.delete_history_before_delete_object(
            HistoryClientModel.__tablename__,
            "client_id",
            client_id,
            "Client",
            "HistoryClient",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "client_id",
            client_id,
            "Client",
            "HistoryClient",
        )
