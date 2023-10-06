from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Client as ClientModel
from src.trackcase_service.utils.commons import (
    copy_objects,
    get_err_msg,
    raise_http_exception,
)

from .schemas import Client as ClientSchema
from .schemas import ClientRequest, ClientResponse


class ClientService(CrudService):
    def __init__(self, db_session: Session):
        super(ClientService, self).__init__(db_session, ClientModel)

    def create_one_client(
        self, request: Request, request_object: ClientRequest
    ) -> ClientResponse:
        try:
            data_model: ClientModel = copy_objects(request_object, ClientModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting Client. Please Try Again!!!", str(ex)),
            )

    def read_one_client(
        self, model_id: int, request: Request, is_include_extras: bool
    ) -> ClientResponse:
        try:
            data_model: ClientModel = super().read_one(model_id)
            if data_model:
                schema_model: ClientSchema = _convert_model_to_schema(
                    data_model, is_include_extras
                )
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Retrieving By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )

    def read_all_clients(
        self, request: Request, is_include_extras: bool
    ) -> ClientResponse:
        try:
            data_models: List[ClientModel] = super().read_all()
            schema_models: List[ClientSchema] = [
                _convert_model_to_schema(c_m, is_include_extras) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving Clients. Please Try Again!!!", str(ex)),
            )

    def update_one_client(
        self, model_id: int, request: Request, request_object: ClientRequest
    ) -> ClientResponse:
        client_response = self.read_one_client(model_id, request, False)

        if not (client_response and client_response.clients):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: ClientModel = copy_objects(request_object, ClientModel)
            data_model = super().update(model_id, data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )

    def delete_one_client(self, model_id: int, request: Request) -> ClientResponse:
        client_response = self.read_one_client(model_id, request, False)

        if not (client_response and client_response.clients):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return ClientResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting By Id: {model_id}. Please Try Again!!!", str(ex)
                ),
            )


def get_client_service(db_session: Session) -> ClientService:
    return ClientService(db_session)


def get_response_single(single: ClientSchema) -> ClientResponse:
    return ClientResponse(clients=[single])


def get_response_multiple(multiple: list[ClientSchema]) -> ClientResponse:
    return ClientResponse(clients=multiple)


def _convert_model_to_schema(
    data_model: ClientModel, is_include_extras: bool = False
) -> ClientSchema:
    data_schema = ClientSchema(
        id=data_model.id,
        created=data_model.created,
        modified=data_model.modified,
        name=data_model.name,
        a_number=data_model.a_number,
        address=data_model.address,
        phone=data_model.phone,
        email=data_model.email,
        judge_id=data_model.judge_id,
    )
    if is_include_extras:
        data_schema.judge = data_model.judge
        data_schema.court_cases = data_model.court_cases
    return data_schema
