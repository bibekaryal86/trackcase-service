from http import HTTPStatus
from typing import List

from fastapi import Request
from sqlalchemy.orm import Session

from src.trackcase_service.db.crud import CrudService
from src.trackcase_service.db.models import HistoryJudge as HistoryJudgeModel
from src.trackcase_service.db.models import Judge as JudgeModel
from src.trackcase_service.db.models import NoteJudge as NoteJudgeModel
from src.trackcase_service.service.history_service import get_history_service
from src.trackcase_service.service.note_service import get_note_service
from src.trackcase_service.service.schemas import Judge as JudgeSchema
from src.trackcase_service.service.schemas import JudgeRequest, JudgeResponse
from src.trackcase_service.utils.commons import (
    check_active_clients,
    get_err_msg,
    raise_http_exception,
)
from src.trackcase_service.utils.constants import get_statuses
from src.trackcase_service.utils.convert import (
    convert_judge_model_to_schema,
    convert_request_schema_to_model,
)


class JudgeService(CrudService):
    def __init__(self, db_session: Session):
        super(JudgeService, self).__init__(db_session, JudgeModel)

    def create_one_judge(
        self, request: Request, request_object: JudgeRequest
    ) -> JudgeResponse:
        try:
            data_model: JudgeModel = convert_request_schema_to_model(
                request_object, JudgeModel
            )
            data_model = super().create(data_model)
            _handle_history(self.db_session, request, data_model.id, request_object)
            schema_model = convert_judge_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Inserting Judge. Please Try Again!!!", str(ex)),
            )

    def read_one_judge(
        self,
        model_id: int,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> JudgeResponse:
        try:
            data_model: JudgeModel = super().read_one(model_id)
            if data_model:
                schema_model: JudgeSchema = convert_judge_model_to_schema(
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
                    f"Error Retrieving Judge By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def read_all_judges(
        self,
        request: Request,
        is_include_extra: bool = False,
        is_include_history: bool = False,
    ) -> JudgeResponse:
        try:
            data_models: List[JudgeModel] = super().read_all()
            schema_models: List[JudgeSchema] = [
                convert_judge_model_to_schema(
                    data_model,
                    is_include_extra,
                    is_include_history,
                )
                for data_model in data_models
            ]
            sorted_schema_models = _sort_judge_by_court_name(schema_models)
            return get_response_multiple(sorted_schema_models)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg("Error Retrieving Judges. Please Try Again!!!", str(ex)),
            )

    def update_one_judge(
        self, model_id: int, request: Request, request_object: JudgeRequest
    ) -> JudgeResponse:
        judge_response = self.read_one_judge(model_id, request, is_include_extra=True)

        if not (judge_response and judge_response.judges):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Judge Not Found By Id: {model_id}!!!",
            )

        _check_dependents_statuses(
            request, request_object.status, judge_response.judges[0]
        )

        try:
            data_model: JudgeModel = convert_request_schema_to_model(
                request_object, JudgeModel
            )
            data_model = super().update(model_id, data_model)
            _handle_history(self.db_session, request, model_id, request_object)
            schema_model = convert_judge_model_to_schema(data_model)
            return get_response_single(schema_model)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Updating Judge By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )

    def delete_one_judge(self, model_id: int, request: Request) -> JudgeResponse:
        judge_response = self.read_one_judge(model_id, request, is_include_extra=True)

        if not (judge_response and judge_response.judges):
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Judge Not Found By Id: {model_id}!!!",
            )

        _check_dependents(request, judge_response.judges[0])
        _handle_history(self.db_session, request, model_id, is_delete=True)

        try:
            super().delete(model_id)
            return JudgeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.SERVICE_UNAVAILABLE,
                get_err_msg(
                    f"Error Deleting Judge By Id: {model_id}. Please Try Again!!!",
                    str(ex),
                ),
            )


def get_judge_service(db_session: Session) -> JudgeService:
    return JudgeService(db_session)


def get_response_single(single: JudgeSchema) -> JudgeResponse:
    return JudgeResponse(judges=[single])


def get_response_multiple(multiple: list[JudgeSchema]) -> JudgeResponse:
    return JudgeResponse(judges=multiple)


def _sort_judge_by_court_name(
    judges: List[JudgeSchema],
) -> List[JudgeSchema]:
    return sorted(
        judges,
        key=lambda x: (x.court.name if x.court else "", x.name if x.name else ""),
    )


def _check_dependents_statuses(
    request: Request,
    status_new: str,
    judge_old: JudgeSchema,
):
    status_old = judge_old.status
    inactive_statuses = get_statuses().get("judge").get("inactive")
    if status_new != status_old and status_new in inactive_statuses:
        if check_active_clients(judge_old.clients):
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Update Judge {judge_old.id} Status to {status_new}, There are Active Clients!",  # noqa: E501
            )


def _check_dependents(request: Request, judge: JudgeSchema):
    if judge.clients:
        raise_http_exception(
            request,
            HTTPStatus.UNPROCESSABLE_ENTITY,
            f"Cannot Delete Judge {judge.id}, There are Linked Clients!",
        )


def _handle_history(
    db_session: Session,
    request: Request,
    judge_id: int,
    request_object: JudgeRequest = None,
    is_delete: bool = False,
):
    history_service = get_history_service(db_session, HistoryJudgeModel)
    if is_delete:
        note_service = get_note_service(db_session, NoteJudgeModel)
        note_service.delete_note_before_delete_object(
            NoteJudgeModel.__tablename__, "judge_id", judge_id, "Judge", "NoteJudge"
        )
        history_service.delete_history_before_delete_object(
            HistoryJudgeModel.__tablename__,
            "judge_id",
            judge_id,
            "Judge",
            "HistoryJudge",
        )
    else:
        history_service.add_to_history(
            request,
            request_object,
            "judge_id",
            judge_id,
            "Judge",
            "HistoryJudge",
        )
