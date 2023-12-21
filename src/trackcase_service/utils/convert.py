from datetime import datetime
from decimal import Decimal
from typing import List

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
    fields = destination_class.__fields__
    required_fields = {
        name: _get_default_value(field) for name, field in fields.items()
    }
    return destination_class(**required_fields)


def _copy_objects(
    source_object, destination_class, destination_object=None, is_copy_all=False
):
    if source_object is None:
        return None
    if destination_object is None:
        destination_object = _create_default_schema_instance(destination_class)
    common_attributes = set(dir(source_object)) & set(dir(destination_object))
    for attr in common_attributes:
        if (
            not callable(getattr(source_object, attr))
            and not attr.startswith("_")
            and (is_copy_all or not getattr(destination_object, attr))
        ):
            value = getattr(source_object, attr)
            if isinstance(value, str):
                trimmed_value = value.strip()
                setattr(destination_object, attr, trimmed_value)
            else:
                setattr(destination_object, attr, value)
    return destination_object


def convert_request_schema_to_model(request_schema, model_class):
    return _copy_objects(request_schema, model_class)


def convert_data_model_to_schema(data_model, schema_class):
    return _copy_objects(data_model, schema_class, is_copy_all=True)


def convert_request_schema_to_history_schema(
    request_schema,
    history_schema_class,
    user_name,
    history_object_id_key,
    history_object_id_value,
):
    history_schema = _copy_objects(request_schema, history_schema_class)
    setattr(history_schema, "user_name", user_name)
    setattr(history_schema, history_object_id_key, history_object_id_value)
    return history_schema


def convert_request_schema_to_note_schema(
    request_schema,
    note_schema_class,
    note_object_id_key,
    note_object_id_value,
):
    note_schema = _copy_objects(request_schema, note_schema_class)
    setattr(note_schema, note_object_id_key, note_object_id_value)
    return note_schema


def convert_note_model_to_note_schema(note_model, note_schema_class):
    return convert_data_model_to_schema(note_model, note_schema_class)


def convert_note_models_to_note_schemas(note_models, note_schema_class):
    note_schemas = []
    if note_models and len(note_models) > 0:
        note_schemas: List[note_schema_class] = [
            convert_note_model_to_note_schema(note_model, note_schema_class)
            for note_model in note_models
        ]
    return note_schemas


def convert_case_collection_model_to_schema(
    data_model: models.CaseCollection,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.CaseCollection:
    data_schema: schemas.CaseCollection = convert_data_model_to_schema(
        data_model, schemas.CaseCollection
    )
    data_schema.note_case_collections = convert_note_models_to_note_schemas(
        data_model.note_case_collections, schemas.NoteCaseCollection
    )
    if is_include_extra_objects:
        data_schema.collection_method = convert_collection_method_model_to_schema(
            data_model.collection_method
        )
        data_schema.court_case = convert_court_case_model_to_schema(
            data_model.court_case
        )
        data_schema.form = convert_form_model_to_schema(data_model.form)
    if is_include_extra_lists:
        if data_model.cash_collections and len(data_model.cash_collections) > 0:
            data_schema.cash_collections = [
                convert_cash_collection_model_to_schema(cash_collection)
                for cash_collection in data_model.cash_collections
            ]
    if is_include_history:
        data_schema.history_case_collections = convert_data_model_to_schema(
            data_model.history_case_collections, schemas.HistoryCaseCollection
        )
    return data_schema


def convert_case_type_model_to_schema(
    data_model: models.CaseType,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.CaseType:
    data_schema: schemas.CaseType = convert_data_model_to_schema(
        data_model, schemas.CaseType
    )
    if is_include_extra_objects:
        pass
    if is_include_extra_lists:
        if data_model.court_cases and len(data_model.court_cases) > 0:
            data_schema.court_cases = [
                convert_court_case_model_to_schema(court_case)
                for court_case in data_model.court_cases
            ]
    if is_include_history:
        pass
    return data_schema


def convert_cash_collection_model_to_schema(
    data_model: models.CashCollection,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.CashCollection:
    data_schema: schemas.CashCollection = convert_data_model_to_schema(
        data_model, schemas.CashCollection
    )
    data_schema.note_cash_collections = convert_note_models_to_note_schemas(
        data_model.note_cash_collections, schemas.NoteCashCollection
    )
    if is_include_extra_objects:
        data_schema.collection_method = convert_collection_method_model_to_schema(
            data_model.collection_method
        )
        data_schema.case_type = convert_case_type_model_to_schema(
            data_model.case_collection
        )
    if is_include_extra_lists:
        pass
    if is_include_history:
        data_schema.history_cash_collections = convert_data_model_to_schema(
            data_model.history_cash_collections, schemas.HistoryCashCollection
        )
    return data_schema


def convert_client_model_to_schema(
    data_model: models.Client,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.Client:
    data_schema: schemas.Client = convert_data_model_to_schema(
        data_model, schemas.Client
    )
    data_schema.note_clients = convert_note_models_to_note_schemas(
        data_model.note_clients, schemas.NoteClient
    )
    if is_include_extra_objects:
        data_schema.judge = convert_judge_model_to_schema(data_model.judge)
    if is_include_extra_lists:
        if data_model.court_cases and len(data_model.court_cases) > 0:
            data_schema.court_cases = [
                convert_court_case_model_to_schema(court_case)
                for court_case in data_model.court_cases
            ]
    if is_include_history:
        data_schema.history_clients = convert_data_model_to_schema(
            data_model.history_clients, schemas.HistoryClient
        )
    return data_schema


def convert_collection_method_model_to_schema(
    data_model: models.CollectionMethod,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.CollectionMethod:
    data_schema: schemas.CollectionMethod = convert_data_model_to_schema(
        data_model, schemas.CollectionMethod
    )
    if is_include_extra_objects:
        pass
    if is_include_extra_lists:
        if data_model.cash_collections and len(data_model.cash_collections) > 0:
            data_schema.cash_collections = [
                convert_cash_collection_model_to_schema(cash_collection)
                for cash_collection in data_model.cash_collections
            ]
        if data_model.case_collections and len(data_model.case_collections) > 0:
            data_schema.case_collections = [
                convert_case_collection_model_to_schema(case_collection)
                for case_collection in data_model.case_collections
            ]
    if is_include_history:
        pass
    return data_schema


def convert_court_case_model_to_schema(
    data_model: models.CourtCase,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.CourtCase:
    data_schema: schemas.CourtCase = convert_data_model_to_schema(
        data_model, schemas.CourtCase
    )
    data_schema.note_court_cases = convert_note_models_to_note_schemas(
        data_model.note_court_cases, schemas.NoteCourtCase
    )
    if is_include_extra_objects:
        data_schema.case_type = convert_case_type_model_to_schema(data_model.case_type)
        data_schema.client = convert_client_model_to_schema(data_model.client)
    if is_include_extra_lists:
        if data_model.forms and len(data_model.forms) > 0:
            data_schema.forms = [
                convert_form_model_to_schema(form) for form in data_model.forms
            ]
        if data_model.case_collections and len(data_model.case_collections) > 0:
            data_schema.case_collections = [
                convert_case_collection_model_to_schema(case_collection)
                for case_collection in data_model.case_collections
            ]
        if data_model.hearing_calendars and len(data_model.hearing_calendars) > 0:
            data_schema.hearing_calendars = [
                convert_hearing_calendar_model_to_schema(hearing_calendar)
                for hearing_calendar in data_model.hearing_calendars
            ]
            data_schema.task_calendars = [
                convert_task_calendar_model_to_schema(task_calendar)
                for task_calendar in data_model.task_calendars
            ]
    if is_include_history:
        data_schema.history_court_cases = convert_data_model_to_schema(
            data_model.history_court_cases, schemas.HistoryCourtCase
        )
    return data_schema


def convert_court_model_to_schema(
    data_model: models.Court,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.Court:
    data_schema: schemas.Court = convert_data_model_to_schema(data_model, schemas.Court)
    data_schema.note_courts = convert_note_models_to_note_schemas(
        data_model.note_courts, schemas.NoteCourt
    )
    if is_include_extra_objects:
        pass
    if is_include_extra_lists:
        if data_model.judges and len(data_model.judges) > 0:
            data_schema.judges = [
                convert_judge_model_to_schema(judge) for judge in data_model.judges
            ]
    if is_include_history:
        data_schema.history_courts = convert_data_model_to_schema(
            data_model.history_courts, schemas.HistoryCourt
        )
    return data_schema


def convert_form_model_to_schema(
    data_model: models.Form,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.Form:
    data_schema: schemas.Form = convert_data_model_to_schema(data_model, schemas.Form)
    data_schema.note_forms = convert_note_models_to_note_schemas(
        data_model.note_forms, schemas.NoteForm
    )
    if is_include_extra_objects:
        data_schema.form_status = convert_form_status_model_to_schema(
            data_model.form_status
        )
        data_schema.form_type = convert_form_type_model_to_schema(data_model.form_type)
        data_schema.task_calendar = convert_task_calendar_model_to_schema(
            data_model.task_calendar
        )
        data_schema.court_case = convert_court_case_model_to_schema(
            data_model.court_case
        )
    if is_include_extra_lists:
        if data_model.case_collections and len(data_model.case_collections) > 0:
            data_schema.case_collections = [
                convert_case_collection_model_to_schema(case_collection)
                for case_collection in data_model.case_collections
            ]
    if is_include_history:
        data_schema.history_forms = convert_data_model_to_schema(
            data_model.history_forms, schemas.HistoryForm
        )
    return data_schema


def convert_form_status_model_to_schema(
    data_model: models.FormStatus,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.FormStatus:
    data_schema: schemas.FormStatus = convert_data_model_to_schema(
        data_model, schemas.FormStatus
    )
    if is_include_extra_objects:
        pass
    if is_include_extra_lists:
        if data_model.forms and len(data_model.forms) > 0:
            data_schema.forms = [
                convert_form_model_to_schema(form) for form in data_model.forms
            ]
    if is_include_history:
        pass
    return data_schema


def convert_form_type_model_to_schema(
    data_model: models.FormType,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.FormType:
    data_schema: schemas.FormType = convert_data_model_to_schema(
        data_model, schemas.FormType
    )
    if is_include_extra_objects:
        pass
    if is_include_extra_lists:
        if data_model.forms and len(data_model.forms) > 0:
            data_schema.forms = [
                convert_form_model_to_schema(form) for form in data_model.forms
            ]
    if is_include_history:
        pass
    return data_schema


def convert_hearing_calendar_model_to_schema(
    data_model: models.HearingCalendar,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.HearingCalendar:
    data_schema: schemas.HearingCalendar = convert_data_model_to_schema(
        data_model, schemas.HearingCalendar
    )
    data_schema.note_hearing_calendars = convert_note_models_to_note_schemas(
        data_model.note_hearing_calendars, schemas.NoteHearingCalendar
    )
    if is_include_extra_objects:
        data_schema.hearing_type = convert_hearing_type_model_to_schema(
            data_model.hearing_type
        )
        data_schema.court_case = convert_court_case_model_to_schema(
            data_model.court_case
        )
    if is_include_extra_lists:
        if data_model.task_calendars and len(data_model.task_calendars) > 0:
            data_schema.task_calendars = [
                convert_task_calendar_model_to_schema(task_calendar)
                for task_calendar in data_model.task_calendars
            ]
    if is_include_history:
        data_schema.history_hearing_calendars = convert_data_model_to_schema(
            data_model.history_hearing_calendars, schemas.HistoryHearingCalendar
        )
    return data_schema


def convert_hearing_type_model_to_schema(
    data_model: models.HearingType,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.HearingType:
    data_schema: schemas.HearingType = convert_data_model_to_schema(
        data_model, schemas.HearingType
    )
    if is_include_extra_objects:
        pass
    if is_include_extra_lists:
        if data_model.hearing_calendars and len(data_model.hearing_calendars) > 0:
            data_schema.hearing_calendars = [
                convert_hearing_calendar_model_to_schema(data_model.hearing_calendars)
            ]
    if is_include_history:
        pass
    return data_schema


def convert_judge_model_to_schema(
    data_model: models.Judge,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.Judge:
    data_schema: schemas.Judge = convert_data_model_to_schema(data_model, schemas.Judge)
    data_schema.note_judges = convert_note_models_to_note_schemas(
        data_model.note_judges, schemas.NoteJudge
    )
    if is_include_extra_objects:
        data_schema.court = convert_court_model_to_schema(data_model.court)
    if is_include_extra_lists:
        if data_model.clients and len(data_model.clients) > 0:
            data_schema.clients = [
                convert_client_model_to_schema(client) for client in data_model.clients
            ]
    if is_include_history:
        data_schema.history_judges = convert_data_model_to_schema(
            data_model.history_judges, schemas.HistoryJudge
        )
    return data_schema


def convert_task_calendar_model_to_schema(
    data_model: models.TaskCalendar,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.TaskCalendar:
    data_schema: schemas.TaskCalendar = convert_data_model_to_schema(
        data_model, schemas.TaskCalendar
    )
    data_schema.note_task_calendars = convert_note_models_to_note_schemas(
        data_model.note_task_calendars, schemas.NoteTaskCalendar
    )
    if is_include_extra_objects:
        data_schema.task_type = convert_task_type_model_to_schema(data_model.task_type)
        data_schema.court_case = convert_court_case_model_to_schema(
            data_model.court_case
        )
        data_schema.hearing_calendar = convert_hearing_calendar_model_to_schema(
            data_model.hearing_calendar
        )
    if is_include_extra_lists:
        if data_model.forms and len(data_model.forms) > 0:
            data_schema.forms = [
                convert_form_model_to_schema(form) for form in data_model.forms
            ]
    if is_include_history:
        data_schema.history_task_calendars = convert_data_model_to_schema(
            data_model.history_task_calendars, schemas.HistoryTaskCalendar
        )
    return data_schema


def convert_task_type_model_to_schema(
    data_model: models.TaskType,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> schemas.TaskType:
    data_schema: schemas.TaskType = convert_data_model_to_schema(
        data_model, schemas.TaskType
    )
    if is_include_extra_objects:
        pass
    if is_include_extra_lists:
        if data_model.task_calendars and len(data_model.task_calendars) > 0:
            data_schema.task_calendars = [
                convert_task_calendar_model_to_schema(task_calendar)
                for task_calendar in data_model.task_calendars
            ]
    if is_include_history:
        pass
    return data_schema
