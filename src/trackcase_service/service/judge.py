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


class JudgeService(CrudService):
    def __init__(self, db_session: Session):
        super(JudgeService, self).__init__(db_session, models.Judge)

    @check_permissions("judges_create")
    def create_judge(
        self, request: Request, request_object: schemas.JudgeRequest
    ) -> schemas.JudgeResponse:
        try:
            data_model: models.Judge = convert_schema_to_model(
                request_object, models.Judge
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryJudge
            ).add_to_history(
                request,
                request_object,
                "judge_id",
                data_model.id,
                "Judge",
                "HistoryJudge",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Judge,
                exclusions=[
                    "clients",
                    "history_judges",
                    "history_clients",
                ],
            )
            return schemas.JudgeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting Judge. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("judges_read")
    def read_judge(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.JudgeResponse:
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
                            f"Judge Not Found By Id: {request_metadata.schema_model_id}!!!",
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
                    schema_class=schemas.Judge,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "clients",
                        "history_judges",
                        "history_clients",
                    ],
                    extra_to_include=["clients"],
                    history_to_include=["history_judges"],
                )
                for data_model in response_data
            ]
            return schemas.JudgeResponse(data=schema_models, metadata=response_metadata)
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving Judge. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    @check_permissions("judges_update")
    def update_judge(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.JudgeRequest,
        is_restore: bool = False,
    ) -> schemas.JudgeResponse:
        judge_old = self.check_judge_exists(model_id, request, is_restore)
        self.check_judge_dependents_statuses(
            request, request_object.component_status_id, judge_old
        )

        try:
            data_model: models.Judge = convert_schema_to_model(
                request_object, models.Judge
            )
            data_model = self.update(model_id, data_model, is_restore)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryJudge
            ).add_to_history(
                request,
                request_object,
                "judge_id",
                data_model.id,
                "Judge",
                "HistoryJudge",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Judge,
                exclusions=[
                    "clients",
                    "history_judges",
                    "history_clients",
                ],
            )
            return schemas.JudgeResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating Judge By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    @check_permissions("judges_delete")
    def delete_judge(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.JudgeResponse:
        judge_old = self.check_judge_exists(model_id, request, is_hard_delete)
        if judge_old.clients:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete Judge {model_id}, There are Linked Clients!",  # noqa: E501
            )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryJudge
            ).delete_history_before_delete_object(
                models.HistoryJudge.__tablename__,
                "judge_id",
                model_id,
                "Judge",
                "HistoryJudge",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryJudge
            ).add_to_history(
                request,
                judge_old,
                "judge_id",
                model_id,
                "Judge",
                "HistoryJudge",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.JudgeResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting Judge By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_judge_exists(
        self, model_id: int, request: Request, is_include_deleted: bool = False
    ) -> schemas.Judge:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id,
            is_include_extra=True,
            is_include_deleted=is_include_deleted,
        )
        judge_response = self.read_judge(request, request_metadata)
        if not judge_response or not judge_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Judge Not Found By Id: {model_id}!!!",
            )
        return judge_response.data[0]

    def check_judge_dependents_statuses(
        self,
        request: Request,
        status_new: int,
        judge_old: schemas.Judge,
    ):
        if judge_old.clients:
            status_old = judge_old.component_status_id
            ref_types_service = get_ref_types_service(
                service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
                db_session=self.db_session,
            )
            judge_active_statuses = ref_types_service.get_component_status(
                request,
                schemas.ComponentStatusNames.JUDGE,
                schemas.ComponentStatusTypes.ACTIVE,
            )
            active_status_ids_judge = [
                component_status.id for component_status in judge_active_statuses
            ]

            if status_new != status_old and status_new not in active_status_ids_judge:
                client_active_statuses = ref_types_service.get_component_status(
                    request,
                    schemas.ComponentStatusNames.CLIENT,
                    schemas.ComponentStatusTypes.ACTIVE,
                )
                active_status_ids_client = [
                    component_status.id for component_status in client_active_statuses
                ]
                if check_active_component_status(
                    judge_old.clients, active_status_ids_client
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update Judge {judge_old.id} Status to {status_new}, There are Active Clients!",  # noqa: E501
                    )


def get_judge_service(db_session: Session) -> JudgeService:
    return JudgeService(db_session)
