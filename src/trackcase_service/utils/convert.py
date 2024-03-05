from datetime import datetime
from decimal import Decimal

from pydantic.fields import FieldInfo

from src.trackcase_service.db import models
from src.trackcase_service.service import schemas


def _get_default_value(field: FieldInfo):
    field_type_name = field.annotation.__name__
    if field.is_required():
        if field_type_name == "str":
            return ""
        elif field_type_name == "int":
            return 0
        elif field_type_name == "datetime":
            return datetime.now()
        elif field_type_name == "Decimal":
            return Decimal("0.00")
        elif field_type_name == "list":
            return []
        elif field_type_name == "bool":
            return False
    return field.default


# this is required because Pydantic doesn't allow creating empty instance
# so create an instance with default empty values according to type
def _create_default_schema_instance(destination_class):
    fields = destination_class.__fields__
    required_fields = {
        name: _get_default_value(field) for name, field in fields.items()
    }
    destination_object = destination_class(**required_fields)
    return destination_object


def _copy_objects(
    source_object,
    destination_class,
    destination_object=None,
    is_copy_all=False,
    exclusions=None,
):
    if exclusions is None:
        exclusions = []
    if source_object is None:
        return None
    if destination_object is None:
        destination_object = _create_default_schema_instance(destination_class)
    common_attributes = set(dir(source_object)) & set(dir(destination_object))
    for attr in common_attributes:
        if (
            not callable(getattr(source_object, attr))
            and not attr.startswith("_")
            and attr not in exclusions
            and (is_copy_all or not getattr(destination_object, attr))
        ):
            value = getattr(source_object, attr)
            if value and isinstance(value, str):
                setattr(destination_object, attr, value.strip().upper())
            elif isinstance(value, bool) or value:
                setattr(destination_object, attr, value)
            else:
                setattr(destination_object, attr, None)
    return destination_object


def convert_schema_to_model(
    request_schema,
    model_class,
    app_user_id=None,
    history_object_id_key=None,
    history_object_id_value=None,
):
    data_model = _copy_objects(request_schema, model_class, model_class())
    if history_object_id_key and history_object_id_value:
        setattr(data_model, "app_user_id", app_user_id)
        setattr(data_model, history_object_id_key, history_object_id_value)
    return data_model


def convert_model_to_schema(
    data_model,
    schema_class,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    exclusions=None,
    extra_to_include=None,
    history_to_include=None,
):
    if extra_to_include is None:
        extra_to_include = []
    if history_to_include is None:
        history_to_include = []
    data_schema = _copy_objects(
        data_model, schema_class, is_copy_all=True, exclusions=exclusions
    )
    if is_include_extra and extra_to_include:
        for extra in extra_to_include:
            setattr(data_schema, extra, getattr(data_model, extra))
    if is_include_history and history_to_include:
        for history in history_to_include:
            setattr(data_schema, history, getattr(data_model, history))
    return data_schema


def convert_data_model_to_schema(data_model, schema_class, exclusions=None):
    return _copy_objects(
        data_model, schema_class, is_copy_all=True, exclusions=exclusions
    )


def convert_case_collection_model_to_schema(
    data_model: models.CaseCollection,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.CaseCollection:
    exclusions = [
        "cash_collections",
        "history_case_collections",
        "history_cash_collections",
    ]
    data_schema: schemas.CaseCollection = convert_data_model_to_schema(
        data_model, schemas.CaseCollection, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "cash_collections", data_model.cash_collections)
    if is_include_history:
        setattr(
            data_schema, "history_case_collections", data_model.history_case_collections
        )
    return data_schema


def convert_cash_collection_model_to_schema(
    data_model: models.CashCollection,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.CashCollection:
    exclusions = ["history_cash_collections"]
    data_schema: schemas.CashCollection = convert_data_model_to_schema(
        data_model, schemas.CashCollection, exclusions
    )
    if is_include_extra:
        pass
    if is_include_history:
        setattr(
            data_schema, "history_cash_collections", data_model.history_cash_collections
        )
    return data_schema


def convert_client_model_to_schema(
    data_model: models.Client,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.Client:
    exclusions = ["court_cases", "history_clients", "history_court_cases"]
    data_schema: schemas.Client = convert_data_model_to_schema(
        data_model, schemas.Client, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "court_cases", data_model.court_cases)
    if is_include_history:
        setattr(data_schema, "history_clients", data_model.history_clients)
    return data_schema


def convert_court_case_model_to_schema(
    data_model: models.CourtCase,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.CourtCase:
    exclusions = [
        "forms",
        "case_collections",
        "hearing_calendars",
        "history_court_cases",
        "history_hearing_calendars",
        "history_forms",
        "history_case_collections",
    ]
    data_schema: schemas.CourtCase = convert_data_model_to_schema(
        data_model, schemas.CourtCase, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "forms", data_model.forms)
        setattr(data_schema, "case_collections", data_model.case_collections)
        setattr(data_schema, "hearing_calendars", data_model.hearing_calendars)
    if is_include_history:
        setattr(data_schema, "history_court_cases", data_model.history_court_cases)
    return data_schema


def convert_court_model_to_schema(
    data_model: models.Court,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.Court:
    exclusions = ["judges", "history_courts", "history_judges"]
    data_schema: schemas.Court = convert_data_model_to_schema(
        data_model, schemas.Court, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "judges", data_model.judges)
    if is_include_history:
        setattr(data_schema, "history_courts", data_model.history_courts)
    return data_schema


def convert_form_model_to_schema(
    data_model: models.Filing,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.Filing:
    exclusions = [
        "task_calendars",
        "history_forms",
        "history_task_calendars",
    ]
    data_schema: schemas.Filing = convert_data_model_to_schema(
        data_model, schemas.Filing, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "task_calendars", data_model.task_calendars)
    if is_include_history:
        setattr(data_schema, "history_forms", data_model.history_forms)
    return data_schema


def convert_hearing_calendar_model_to_schema(
    data_model: models.HearingCalendar,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.HearingCalendar:
    exclusions = [
        "task_calendars",
        "history_hearing_calendars",
        "history_task_calendars",
    ]
    data_schema: schemas.HearingCalendar = convert_data_model_to_schema(
        data_model, schemas.HearingCalendar, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "task_calendars", data_model.task_calendars)
    if is_include_history:
        setattr(
            data_schema,
            "history_hearing_calendars",
            data_model.history_hearing_calendars,
        )
    return data_schema


def convert_judge_model_to_schema(
    data_model: models.Judge,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.Judge:
    exclusions = ["clients", "history_judges", "history_clients"]
    data_schema: schemas.Judge = convert_data_model_to_schema(
        data_model, schemas.Judge, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "clients", data_model.clients)
    if is_include_history:
        setattr(data_schema, "history_judges", data_model.history_judges)
    return data_schema


def convert_task_calendar_model_to_schema(
    data_model: models.TaskCalendar,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.TaskCalendar:
    exclusions = ["history_task_calendars", "history_forms"]
    data_schema: schemas.TaskCalendar = convert_data_model_to_schema(
        data_model, schemas.TaskCalendar, exclusions
    )
    if is_include_extra:
        pass
    if is_include_history:
        setattr(
            data_schema, "history_task_calendars", data_model.history_task_calendars
        )
    return data_schema
