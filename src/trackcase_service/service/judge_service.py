from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import Judge as JudgeModel
from src.trackcase_service.utils.commons import copy_objects, raise_http_exception

from .schemas import Judge as JudgeSchema
from .schemas import JudgeRequest, JudgeResponse


class JudgeService(CrudService):
    def __init__(self, db_session: Session):
        super(JudgeService, self).__init__(db_session, JudgeModel)

    def create_one_judge(
        self, request: Request, request_object: JudgeRequest
    ) -> JudgeResponse:
        try:
            data_model: JudgeModel = copy_objects(request_object, JudgeModel)
            data_model = super().create(data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Inserting Judge. Please Try Again!!!",
                str(ex),
            )

    def read_one_judge(self, model_id: int, request: Request) -> JudgeResponse:
        try:
            data_model: JudgeModel = super().read_one(model_id)
            if data_model:
                schema_model: JudgeSchema = _convert_model_to_schema(data_model)
                return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Retrieving By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def read_all_judges(self, request: Request) -> JudgeResponse:
        try:
            data_models: List[JudgeModel] = super().read_all()
            schema_models: List[JudgeSchema] = [
                _convert_model_to_schema(c_m) for c_m in data_models
            ]
            return get_response_multiple(schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                "Error Retrieving Judges. Please Try Again!!!",
                str(ex),
            )

    def update_one_judge(
        self, model_id: int, request: Request, request_object: JudgeRequest
    ) -> JudgeResponse:
        judge_response = self.read_one_judge(model_id, request)

        if not (judge_response and judge_response.judges):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            data_model: JudgeModel = copy_objects(request_object, JudgeModel)
            data_model = super().update(model_id, data_model)
            schema_model = _convert_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Updating By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )

    def delete_one_judge(self, model_id: int, request: Request) -> JudgeResponse:
        judge_response = self.read_one_judge(model_id, request)

        if not (judge_response and judge_response.judges):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Not Found By Id: {model_id}!!!",
                f"Not Found By Id: {model_id}!!!",
            )

        try:
            super().delete(model_id)
            return JudgeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                f"Error Deleting By Id: {model_id}. Please Try Again!!!",
                str(ex),
            )


def get_judge_service(db_session: Session) -> JudgeService:
    return JudgeService(db_session)


def get_response_single(single: JudgeSchema) -> JudgeResponse:
    return JudgeResponse(judges=[single])


def get_response_multiple(multiple: list[JudgeSchema]) -> JudgeResponse:
    return JudgeResponse(judges=multiple)


def _convert_model_to_schema(data_model: JudgeModel) -> JudgeSchema:
    data_schema = JudgeSchema(
        name=data_model.name,
        address=data_model.address,
        dhs_address=data_model.dhs_address,
    )
    data_schema = copy_objects(data_model, JudgeSchema, data_schema)
    return data_schema
