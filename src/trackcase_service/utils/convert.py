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
    return field.default


# this is required because Pydantic doesn't allow creating empty instance
# so create an instance with default empty values according to type
def _create_default_schema_instance(destination_class):
    is_allow_empty_status = hasattr(destination_class, "allow_empty_status")
    if is_allow_empty_status:
        destination_class.allow_empty_status = True
    fields = destination_class.__fields__
    required_fields = {
        name: _get_default_value(field) for name, field in fields.items()
    }
    destination_object = destination_class(**required_fields)
    if is_allow_empty_status:
        destination_class.allow_empty_status = False
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
                trimmed_value = value.strip()
                setattr(destination_object, attr, trimmed_value)
            elif value:
                setattr(destination_object, attr, value)
            else:
                setattr(destination_object, attr, None)
    return destination_object


def convert_request_schema_to_model(request_schema, model_class):
    return _copy_objects(request_schema, model_class, model_class())


def convert_data_model_to_schema(data_model, schema_class, exclusions=None):
    return _copy_objects(
        data_model, schema_class, is_copy_all=True, exclusions=exclusions
    )


def convert_request_schema_to_history_model(
    request_schema,
    history_model_class,
    user_name,
    history_object_id_key,
    history_object_id_value,
):
    history_model = _copy_objects(
        request_schema, history_model_class, history_model_class()
    )
    setattr(history_model, "user_name", user_name)
    setattr(history_model, history_object_id_key, history_object_id_value)
    return history_model


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


def convert_case_type_model_to_schema(
    data_model: models.CaseType,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.CaseType:
    exclusions = ["court_cases", "history_court_cases"]
    data_schema: schemas.CaseType = convert_data_model_to_schema(
        data_model, schemas.CaseType, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "court_cases", data_model.court_cases)
    if is_include_history:
        pass
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


def convert_collection_method_model_to_schema(
    data_model: models.CollectionMethod,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.CollectionMethod:
    exclusions = [
        "cash_collections",
        "case_collections",
        "history_cash_collections",
        "history_case_collections",
    ]
    data_schema: schemas.CollectionMethod = convert_data_model_to_schema(
        data_model, schemas.CollectionMethod, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "cash_collections", data_model.cash_collections)
        setattr(data_schema, "case_collections", data_model.case_collections)
    if is_include_history:
        pass
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
        "task_calendars",
        "history_court_cases",
        "history_hearing_calendars",
        "history_task_calendars",
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
        setattr(data_schema, "task_calendars", data_model.task_calendars)
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
    data_model: models.Form,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.Form:
    exclusions = ["case_collections", "history_forms", "history_case_collections"]
    data_schema: schemas.Form = convert_data_model_to_schema(
        data_model, schemas.Form, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "case_collections", data_model.case_collections)
    if is_include_history:
        setattr(data_schema, "history_forms", data_model.history_forms)
    return data_schema


def convert_form_type_model_to_schema(
    data_model: models.FormType,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.FormType:
    exclusions = ["forms", "history_forms"]
    data_schema: schemas.FormType = convert_data_model_to_schema(
        data_model, schemas.FormType, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "forms", data_model.forms)
    if is_include_history:
        pass
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


def convert_hearing_type_model_to_schema(
    data_model: models.HearingType,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.HearingType:
    exclusions = ["hearing_calendars", "history_hearing_calendars"]
    data_schema: schemas.HearingType = convert_data_model_to_schema(
        data_model, schemas.HearingType, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "hearing_calendars", data_model.hearing_calendars)
    if is_include_history:
        pass
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
    exclusions = ["forms", "history_task_calendars", "history_forms"]
    data_schema: schemas.TaskCalendar = convert_data_model_to_schema(
        data_model, schemas.TaskCalendar, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "forms", data_model.forms)
    if is_include_history:
        setattr(
            data_schema, "history_task_calendars", data_model.history_task_calendars
        )
    return data_schema


def convert_task_type_model_to_schema(
    data_model: models.TaskType,
    is_include_extra=False,
    is_include_history=False,
) -> schemas.TaskType:
    exclusions = ["task_calendars", "history_task_calendars"]
    data_schema: schemas.TaskType = convert_data_model_to_schema(
        data_model, schemas.TaskType, exclusions
    )
    if is_include_extra:
        setattr(data_schema, "task_calendars", data_model.task_calendars)
    if is_include_history:
        pass
    return data_schema


def convert_note_request_to_note_model(
    note_object_type: str, note_request: schemas.NoteRequest = None
):
    note_class = None
    note_model = None
    match note_object_type:
        case "court":
            note_class = models.NoteCourt
            if note_request:
                note_model = models.NoteCourt()
                note_model.court_id = note_request.note_object_id
        case "judge":
            note_class = models.NoteJudge
            if note_request:
                note_model = models.NoteJudge()
                note_model.judge_id = note_request.note_object_id
        case "client":
            note_class = models.NoteClient
            if note_request:
                note_model = models.NoteClient()
                note_model.client_id = note_request.note_object_id
        case "court_case":
            note_class = models.NoteCourtCase
            if note_request:
                note_model = models.NoteCourtCase()
                note_model.court_case_id = note_request.note_object_id
        case "hearing_calendar":
            note_class = models.NoteHearingCalendar
            if note_request:
                note_model = models.NoteHearingCalendar()
                note_model.hearing_calendar_id = note_request.note_object_id
        case "task_calendar":
            note_class = models.NoteTaskCalendar
            if note_request:
                note_model = models.NoteTaskCalendar()
                note_model.task_calendar_id = note_request.note_object_id
        case "form":
            note_class = models.NoteForm
            if note_request:
                note_model = models.NoteForm()
                note_model.form_id = note_request.note_object_id
        case "case_collection":
            note_class = models.NoteCaseCollection
            if note_request:
                note_model = models.NoteCaseCollection()
                note_model.case_collection_id = note_request.note_object_id
        case "cash_collection":
            note_class = models.NoteCashCollection
            if note_request:
                note_model = models.NoteCashCollection()
                note_model.cash_collection_id = note_request.note_object_id
    if note_model:
        note_model.user_name = note_request.user_name
        note_model.note = note_request.note
    return note_class, note_model
