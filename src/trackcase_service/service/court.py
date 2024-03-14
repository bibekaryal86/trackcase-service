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
    get_err_msg,
    get_read_response_data_metadata,
    raise_http_exception,
)
from src.trackcase_service.utils.convert import (
    convert_model_to_schema,
    convert_schema_to_model,
)


class CourtService(CrudService):
    def __init__(self, db_session: Session):
        super(CourtService, self).__init__(db_session, models.Court)

    def create_court(
        self, request: Request, request_object: schemas.CourtRequest
    ) -> schemas.CourtResponse:
        try:
            data_model: models.Court = convert_schema_to_model(
                request_object, models.Court
            )
            data_model = self.create(data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourt
            ).add_to_history(
                request,
                request_object,
                "court_id",
                data_model.id,
                "Court",
                "HistoryCourt",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Court,
                exclusions=[
                    "judges",
                    "history_courts",
                    "history_judges",
                ],
            )
            return schemas.CourtResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Inserting Court. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def read_court(
        self, request: Request, request_metadata: schemas.RequestMetadata = None
    ) -> schemas.CourtResponse:
        try:
            if request_metadata:
                if request_metadata.model_id:
                    read_response = self.read(
                        model_id=request_metadata.model_id,
                        is_include_soft_deleted=request_metadata.is_include_deleted,
                    )
                    response_data, response_metadata = get_read_response_data_metadata(
                        read_response
                    )
                    if not response_data:
                        raise_http_exception(
                            request,
                            HTTPStatus.NOT_FOUND,
                            f"Court Not Found By Id: {request_metadata.model_id}!!!",
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
                    schema_class=schemas.Court,
                    is_include_extra=request_metadata.is_include_extra,
                    is_include_history=request_metadata.is_include_history,
                    exclusions=[
                        "judges",
                        "history_courts",
                        "history_judges",
                    ],
                    extra_to_include=["judges"],
                    history_to_include=["history_courts"],
                )
                for data_model in response_data
            ]
            return schemas.CourtResponse(data=schema_models, metadata=response_metadata)
        except Exception as ex:
            if isinstance(ex, HTTPException):
                raise
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg("Error Retrieving Court. Please Try Again!!!", str(ex)),
                exc_info=sys.exc_info(),
            )

    def update_court(
        self,
        model_id: int,
        request: Request,
        request_object: schemas.CourtRequest,
    ) -> schemas.CourtResponse:
        court_old = self.check_court_exists(model_id, request)
        self.check_court_dependents_statuses(
            request, request_object.component_status_id, court_old
        )

        try:
            data_model: models.Court = convert_schema_to_model(
                request_object, models.Court
            )
            data_model = self.update(model_id, data_model)
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourt
            ).add_to_history(
                request,
                request_object,
                "court_id",
                data_model.id,
                "Court",
                "HistoryCourt",
            )
            schema_model = convert_model_to_schema(
                data_model,
                schemas.Court,
                exclusions=[
                    "judges",
                    "history_courts",
                    "history_judges",
                ],
            )
            return schemas.CourtResponse(data=[schema_model])
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Updating Court By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def delete_court(
        self, model_id: int, is_hard_delete: bool, request: Request
    ) -> schemas.CourtResponse:
        court_old = self.check_court_exists(model_id, request, is_hard_delete)
        if court_old.judges:
            raise_http_exception(
                request,
                HTTPStatus.UNPROCESSABLE_ENTITY,
                f"Cannot Delete Court {model_id}, There are Linked Judges!",  # noqa: E501
            )

        if is_hard_delete:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourt
            ).delete_history_before_delete_object(
                models.HistoryCourt.__tablename__,
                "court_id",
                model_id,
                "Court",
                "HistoryCourt",
            )
        else:
            get_history_service(
                db_session=self.db_session, db_model=models.HistoryCourt
            ).add_to_history(
                request,
                court_old,
                "court_id",
                model_id,
                "Court",
                "HistoryCourt",
            )

        try:
            self.delete(model_id, is_hard_delete)
            return schemas.CourtResponse(delete_count=1)
        except Exception as ex:
            raise_http_exception(
                request,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                get_err_msg(
                    f"Error Deleting Court By Id: {model_id}. Please Try Again!!!",  # noqa: E501
                    str(ex),
                ),
                exc_info=sys.exc_info(),
            )

    def check_court_exists(self, model_id: int, request: Request, is_include_deleted: bool = False) -> schemas.Court:
        request_metadata = schemas.RequestMetadata(
            model_id=model_id, is_include_extra=True, is_include_deleted=is_include_deleted
        )
        court_response = self.read_court(request, request_metadata)
        if not court_response or not court_response.data:
            raise_http_exception(
                request,
                HTTPStatus.NOT_FOUND,
                f"Court Not Found By Id: {model_id}!!!",
            )
        return court_response.data[0]

    def check_court_dependents_statuses(
        self,
        request: Request,
        status_new: int,
        court_old: schemas.Court,
    ):
        if court_old.judges:
            status_old = court_old.component_status_id
            ref_types_service = get_ref_types_service(
                service_type=schemas.RefTypesServiceRegistry.COMPONENT_STATUS,
                db_session=self.db_session,
            )
            court_active_statuses = ref_types_service.get_component_status(
                request,
                schemas.ComponentStatusNames.COURT,
                schemas.ComponentStatusTypes.ACTIVE,
            )
            active_status_ids_court = [
                component_status.id for component_status in court_active_statuses
            ]

            if status_new != status_old and status_new not in active_status_ids_court:
                judge_active_statuses = ref_types_service.get_component_status(
                    request,
                    schemas.ComponentStatusNames.JUDGE,
                    schemas.ComponentStatusTypes.ACTIVE,
                )
                active_status_ids_judge = [
                    component_status.id for component_status in judge_active_statuses
                ]
                if check_active_component_status(
                    court_old.judges, active_status_ids_judge
                ):
                    raise_http_exception(
                        request,
                        HTTPStatus.UNPROCESSABLE_ENTITY,
                        f"Cannot Update Court {court_old.id} Status to {status_new}, There are Active Judges!",  # noqa: E501
                    )


def get_court_service(db_session: Session) -> CourtService:
    return CourtService(db_session)
