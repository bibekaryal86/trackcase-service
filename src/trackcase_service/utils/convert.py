from typing import List

from src.trackcase_service.db.models import CaseCollection as CaseCollectionModel
from src.trackcase_service.db.models import CaseType as CaseTypeModel
from src.trackcase_service.db.models import CashCollection as CashCollectionModel
from src.trackcase_service.db.models import Client as ClientModel
from src.trackcase_service.db.models import CollectionMethod as CollectionMethodModel
from src.trackcase_service.db.models import Court as CourtModel
from src.trackcase_service.db.models import CourtCase as CourtCaseModel
from src.trackcase_service.db.models import Form as FormModel
from src.trackcase_service.db.models import FormStatus as FormStatusModel
from src.trackcase_service.db.models import FormType as FormTypeModel
from src.trackcase_service.db.models import HearingCalendar as HearingCalendarModel
from src.trackcase_service.db.models import HearingType as HearingTypeModel
from src.trackcase_service.db.models import Judge as JudgeModel
from src.trackcase_service.db.models import TaskCalendar as TaskCalendarModel
from src.trackcase_service.db.models import TaskType as TaskTypeModel
from src.trackcase_service.service.schemas import CaseCollection as CaseCollectionSchema
from src.trackcase_service.service.schemas import CaseType as CaseTypeSchema
from src.trackcase_service.service.schemas import CashCollection as CashCollectionSchema
from src.trackcase_service.service.schemas import Client as ClientSchema
from src.trackcase_service.service.schemas import (
    CollectionMethod as CollectionMethodSchema,
)
from src.trackcase_service.service.schemas import Court as CourtSchema
from src.trackcase_service.service.schemas import CourtCase as CourtCaseSchema
from src.trackcase_service.service.schemas import Form as FormSchema
from src.trackcase_service.service.schemas import FormStatus as FormStatusSchema
from src.trackcase_service.service.schemas import FormType as FormTypeSchema
from src.trackcase_service.service.schemas import (
    HearingCalendar as HearingCalendarSchema,
)
from src.trackcase_service.service.schemas import HearingType as HearingTypeSchema
from src.trackcase_service.service.schemas import Judge as JudgeSchema
from src.trackcase_service.service.schemas import (
    NoteCaseCollection as NoteCaseCollectionSchema,
)
from src.trackcase_service.service.schemas import (
    NoteCashCollection as NoteCashCollectionSchema,
)
from src.trackcase_service.service.schemas import NoteClient as NoteClientSchema
from src.trackcase_service.service.schemas import NoteCourt as NoteCourtSchema
from src.trackcase_service.service.schemas import NoteCourtCase as NoteCourtCaseSchema
from src.trackcase_service.service.schemas import NoteForm as NoteFormSchema
from src.trackcase_service.service.schemas import (
    NoteHearingCalendar as NoteHearingCalendarSchema,
)
from src.trackcase_service.service.schemas import NoteJudge as NoteJudgeSchema
from src.trackcase_service.service.schemas import (
    NoteTaskCalendar as NoteTaskCalendarSchema,
)
from src.trackcase_service.service.schemas import TaskCalendar as TaskCalendarSchema
from src.trackcase_service.service.schemas import TaskType as TaskTypeSchema


def _copy_objects(
    source_object, destination_class, destination_object=None, is_copy_all=False
):
    if source_object is None:
        return None
    if destination_object is None:
        destination_object = destination_class()
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
    data_model: CaseCollectionModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> CaseCollectionSchema:
    data_schema: CaseCollectionSchema = convert_data_model_to_schema(
        data_model, CaseCollectionSchema
    )
    data_schema.note_case_collections = convert_note_models_to_note_schemas(
        data_model.note_case_collections, NoteCaseCollectionSchema
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
        print("extra lists")
    if is_include_history:
        print("history")
    return data_schema


def convert_case_type_model_to_schema(
    data_model: CaseTypeModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> CaseTypeSchema:
    data_schema: CaseTypeSchema = convert_data_model_to_schema(
        data_model, CaseTypeSchema
    )
    if is_include_extra_objects:
        print("extra objects")
    if is_include_extra_lists:
        if data_schema.court_cases and len(data_schema.court_cases) > 0:
            data_schema.court_cases = [
                convert_court_case_model_to_schema(court_case)
                for court_case in data_model.court_cases
            ]
    if is_include_history:
        print("history")
    return data_schema


def convert_cash_collection_model_to_schema(
    data_model: CashCollectionModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> CashCollectionSchema:
    data_schema: CashCollectionSchema = convert_data_model_to_schema(
        data_model, CashCollectionSchema
    )
    data_schema.note_cash_collections = convert_note_models_to_note_schemas(
        data_model.note_cash_collections, NoteCashCollectionSchema
    )
    if is_include_extra_objects:
        data_schema.collection_method = convert_collection_method_model_to_schema(
            data_model.collection_method
        )
        data_schema.case_type = convert_case_type_model_to_schema(
            data_model.case_collection
        )
    if is_include_extra_lists:
        print("extra lists")
    if is_include_history:
        print("history")
    return data_schema


def convert_client_model_to_schema(
    data_model: ClientModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> ClientSchema:
    data_schema: ClientSchema = convert_data_model_to_schema(data_model, ClientSchema)
    data_schema.note_clients = convert_note_models_to_note_schemas(
        data_model.note_clients, NoteClientSchema
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
        print("history")
    return data_schema


def convert_collection_method_model_to_schema(
    data_model: CollectionMethodModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> CollectionMethodSchema:
    data_schema: CollectionMethodSchema = convert_data_model_to_schema(
        data_model, CollectionMethodSchema
    )
    if is_include_extra_objects:
        print("extra objects")
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
        print("history")
    return data_schema


def convert_court_case_model_to_schema(
    data_model: CourtCaseModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> CourtCaseSchema:
    data_schema: CourtCaseSchema = convert_data_model_to_schema(
        data_model, CourtCaseSchema
    )
    data_schema.note_court_cases = convert_note_models_to_note_schemas(
        data_model.note_court_cases, NoteCourtCaseSchema
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
        print("history")
    return data_schema


def convert_court_model_to_schema(
    data_model: CourtModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> CourtSchema:
    data_schema: CourtSchema = convert_data_model_to_schema(data_model, CourtSchema)
    data_schema.note_courts = convert_note_models_to_note_schemas(
        data_model.note_courts, NoteCourtSchema
    )
    if is_include_extra_objects:
        print("extra objects")
    if is_include_extra_lists:
        if data_model.judges and len(data_model.judges) > 0:
            data_schema.judges = [
                convert_judge_model_to_schema(judge) for judge in data_model.judges
            ]
    if is_include_history:
        print("history")
    return data_schema


def convert_form_model_to_schema(
    data_model: FormModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> FormSchema:
    data_schema: FormSchema = convert_data_model_to_schema(data_model, FormSchema)
    data_schema.note_forms = convert_note_models_to_note_schemas(
        data_model.note_forms, NoteFormSchema
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
        print("history")
    return data_schema


def convert_form_status_model_to_schema(
    data_model: FormStatusModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> FormStatusSchema:
    data_schema: FormStatusSchema = convert_data_model_to_schema(
        data_model, FormStatusSchema
    )
    if is_include_extra_objects:
        print("extra objects")
    if is_include_extra_lists:
        if data_model.forms and len(data_model.forms) > 0:
            data_schema.forms = [
                convert_form_model_to_schema(form) for form in data_model.forms
            ]
    if is_include_history:
        print("history")
    return data_schema


def convert_form_type_model_to_schema(
    data_model: FormTypeModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> FormTypeSchema:
    data_schema: FormTypeSchema = convert_data_model_to_schema(
        data_model, FormTypeSchema
    )
    if is_include_extra_objects:
        print("extra objects")
    if is_include_extra_lists:
        if data_model.forms and len(data_model.forms) > 0:
            data_schema.forms = [
                convert_form_model_to_schema(form) for form in data_model.forms
            ]
    if is_include_history:
        print("history")
    return data_schema


def convert_hearing_calendar_model_to_schema(
    data_model: HearingCalendarModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> HearingCalendarSchema:
    data_schema: HearingCalendarSchema = convert_data_model_to_schema(
        data_model, HearingCalendarSchema
    )
    data_schema.note_hearing_calendars = convert_note_models_to_note_schemas(
        data_model.note_hearing_calendars, NoteHearingCalendarSchema
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
        print("history")
    return data_schema


def convert_hearing_type_model_to_schema(
    data_model: HearingTypeModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> HearingTypeSchema:
    data_schema: HearingTypeSchema = convert_data_model_to_schema(
        data_model, HearingTypeSchema
    )
    if is_include_extra_objects:
        print("extra objects")
    if is_include_extra_lists:
        if data_model.hearing_calendars and len(data_model.hearing_calendars) > 0:
            data_schema.hearing_calendars = [
                convert_hearing_calendar_model_to_schema(data_model.hearing_calendars)
            ]
    if is_include_history:
        print("history")
    return data_schema


def convert_judge_model_to_schema(
    data_model: JudgeModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> JudgeSchema:
    data_schema: JudgeSchema = convert_data_model_to_schema(data_model, JudgeSchema)
    data_schema.note_judges = convert_note_models_to_note_schemas(
        data_model.note_judges, NoteJudgeSchema
    )
    if is_include_extra_objects:
        data_schema.court = convert_court_model_to_schema(data_model.court)
    if is_include_extra_lists:
        if data_model.clients and len(data_model.clients) > 0:
            data_schema.clients = [
                convert_client_model_to_schema(client) for client in data_model.clients
            ]
    if is_include_history:
        print("history")
    return data_schema


def convert_task_calendar_model_to_schema(
    data_model: TaskCalendarModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> TaskCalendarSchema:
    data_schema: TaskCalendarSchema = convert_data_model_to_schema(
        data_model, TaskCalendarSchema
    )
    data_schema.note_task_calendars = convert_note_models_to_note_schemas(
        data_model.note_task_calendars, NoteTaskCalendarSchema
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
        print("history")
    return data_schema


def convert_task_type_model_to_schema(
    data_model: TaskTypeModel,
    is_include_extra_objects=False,
    is_include_extra_lists=False,
    is_include_history=False,
) -> TaskTypeSchema:
    data_schema: TaskTypeSchema = convert_data_model_to_schema(
        data_model, TaskTypeSchema
    )
    if is_include_extra_objects:
        print("extra objects")
    if is_include_extra_lists:
        if data_model.task_calendars and len(data_model.task_calendars) > 0:
            data_schema.task_calendars = [
                convert_task_calendar_model_to_schema(task_calendar)
                for task_calendar in data_model.task_calendars
            ]
    if is_include_history:
        print("history")
    return data_schema
