from datetime import datetime
from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict, condecimal, field_validator
from pydantic.alias_generators import to_camel

from src.trackcase_service.utils.constants import get_statuses


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class BaseModelSchema(BaseSchema):
    id: Optional[int] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None


class ErrorDetail(BaseSchema):
    error: Optional[str] = None


class ResponseBase(BaseSchema):
    delete_count: Optional[int] = 0
    detail: Optional[ErrorDetail] = None


class NameDescBase:
    name: str
    description: str


class StatusBase(BaseSchema):
    status: str
    comments: Optional[str] = None


class AddressBase(BaseSchema):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None


class NoteBase(BaseSchema):
    user_name: str
    note: str


class NoteRequest(NoteBase):
    note_object_id: int


class NoteResponse(ResponseBase):
    success: bool


# form type
class FormTypeBase(NameDescBase):
    pass


class FormType(FormTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    forms: list["Form"] = []


class FormTypeRequest(FormTypeBase, BaseSchema):
    pass


class FormTypeResponse(ResponseBase):
    form_types: list[FormType] = []


# collection method
class CollectionMethodBase(NameDescBase):
    pass


class CollectionMethod(CollectionMethodBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    cash_collections: list["CashCollection"] = []
    case_collections: list["CaseCollection"] = []


class CollectionMethodRequest(CollectionMethodBase, BaseSchema):
    pass


class CollectionMethodResponse(ResponseBase):
    collection_methods: list[CollectionMethod] = []


# hearing type
class HearingTypeBase(NameDescBase):
    pass


class HearingType(HearingTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    hearing_calendars: list["HearingCalendar"] = []


class HearingTypeRequest(HearingTypeBase, BaseSchema):
    pass


class HearingTypeResponse(ResponseBase):
    hearing_types: list[HearingType] = []


# task type
class TaskTypeBase(NameDescBase):
    pass


class TaskType(TaskTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    task_calendars: list["TaskCalendar"] = []


class TaskTypeRequest(TaskTypeBase, BaseSchema):
    pass


class TaskTypeResponse(ResponseBase):
    task_types: list[TaskType] = []


# case type
class CaseTypeBase(NameDescBase):
    pass


class CaseType(CaseTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court_cases: list["CourtCase"] = []


class CaseTypeRequest(CaseTypeBase, BaseSchema):
    pass


class CaseTypeResponse(ResponseBase):
    case_types: list[CaseType] = []


# court
class CourtBase(AddressBase, StatusBase):
    name: str
    dhs_address: Optional[str] = None

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("court").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class Court(CourtBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    judges: list["Judge"] = []
    note_courts: list["NoteCourt"] = []
    history_courts: list["HistoryCourt"] = []


class NoteCourt(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court_id: int
    court: Optional[Court] = None


class HistoryCourt(Court):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    court_id: int
    court: Optional[Court] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None


class CourtRequest(CourtBase, BaseSchema):
    pass


class CourtResponse(ResponseBase):
    courts: list[Court] = []


# judge
class JudgeBase(StatusBase):
    name: str
    webex: Optional[str] = None
    court_id: int

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("judge").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class Judge(JudgeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court: Optional[Court] = None
    clients: list["Client"] = []
    note_judges: list["NoteJudge"] = []
    history_judges: list["HistoryJudge"] = []


class NoteJudge(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    judge_id: int
    judge: Optional[Judge] = None


class HistoryJudge(Judge):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    judge_id: int
    judge: Optional[Judge] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None
    court_id: Optional[int] = None


class JudgeRequest(JudgeBase, BaseSchema):
    pass


class JudgeResponse(ResponseBase):
    judges: list[Judge] = []


# client
class ClientBase(AddressBase, StatusBase):
    name: str
    a_number: Optional[str] = None
    email: Optional[str] = None
    judge_id: Optional[int] = None

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("client").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class Client(ClientBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    judge: Optional[Judge] = None
    court_cases: list["CourtCase"] = []
    note_clients: list["NoteClient"] = []
    history_clients: list["HistoryClient"] = []


class NoteClient(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    client_id: int
    client: Optional[Client] = None


class HistoryClient(Client):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    client_id: int
    client: Optional[Client] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None


class ClientRequest(ClientBase, BaseSchema):
    pass


class ClientResponse(ResponseBase):
    clients: list[Client] = []


# court_case
class CourtCaseBase(StatusBase):
    case_type_id: int
    client_id: int

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("court_case").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class CourtCase(CourtCaseBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    case_type: Optional[CaseType] = None
    client: Optional[Client] = None
    forms: list["Form"] = []
    case_collections: list["CaseCollection"] = []
    hearing_calendars: list["HearingCalendar"] = []
    note_court_cases: list["NoteCourtCase"] = []
    history_court_cases: list["HistoryCourtCase"] = []


class NoteCourtCase(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court_case_id: int
    court_case: Optional[CourtCase] = None


class HistoryCourtCase(CourtCase):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    court_case_id: int
    court_case: Optional[CourtCase] = None
    # make NOT optional inherited fields optional in history
    case_type_id: Optional[int] = None
    client_id: Optional[int] = None


class CourtCaseRequest(CourtCaseBase, BaseSchema):
    pass


class CourtCaseResponse(ResponseBase):
    court_cases: list[CourtCase] = []


# hearing_calendar
class HearingCalendarBase(StatusBase):
    hearing_date: datetime
    hearing_type_id: int
    court_case_id: int

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("hearing_calendar").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class HearingCalendar(HearingCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    hearing_type: Optional[HearingType] = None
    court_case: Optional[CourtCase] = None
    task_calendars: list["TaskCalendar"] = []
    note_hearing_calendars: list["NoteHearingCalendar"] = []
    history_hearing_calendars: list["HistoryHearingCalendar"] = []


class NoteHearingCalendar(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    hearing_calendar_id: int
    hearing_calendar: Optional[HearingCalendar] = None


class HistoryHearingCalendar(HearingCalendar):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    hearing_calendar_id: int
    hearing_calendar: Optional[HearingCalendar] = None
    # make NOT optional inherited fields optional in history
    hearing_date: Optional[datetime] = None
    hearing_type_id: Optional[int] = None
    court_case_id: Optional[int] = None


class HearingCalendarRequest(HearingCalendarBase, BaseSchema):
    pass


class HearingCalendarResponse(ResponseBase):
    hearing_calendars: list[HearingCalendar] = []


# task_calendar
class TaskCalendarBase(StatusBase):
    task_date: datetime
    due_date: datetime
    task_type_id: int
    hearing_calendar_id: Optional[int] = None
    form_id: Optional[int] = None

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("task_calendar").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class TaskCalendar(TaskCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    task_type: Optional[TaskType] = None
    hearing_calendar: Optional[HearingCalendar] = None
    form: Optional["Form"] = None
    note_task_calendars: list["NoteTaskCalendar"] = []
    history_task_calendars: list["HistoryTaskCalendar"] = []


class NoteTaskCalendar(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    task_calendar_id: int
    task_calendar: Optional[TaskCalendar] = None


class HistoryTaskCalendar(TaskCalendar):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    task_calendar_id: int
    task_calendar: Optional[TaskCalendar] = None
    # make NOT optional inherited fields optional in history
    task_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    task_type_id: Optional[int] = None


class TaskCalendarRequest(TaskCalendarBase, BaseSchema):
    pass


class TaskCalendarResponse(ResponseBase):
    task_calendars: list[TaskCalendar] = []


# form
class FormBase(StatusBase):
    form_type_id: int
    court_case_id: int
    submit_date: Optional[datetime] = None
    receipt_date: Optional[datetime] = None
    receipt_number: Optional[str] = None
    priority_date: Optional[datetime] = None
    rfe_date: Optional[datetime] = None
    rfe_submit_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("form").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class Form(FormBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    form_type: Optional[FormType] = None
    court_case: Optional[CourtCase] = None
    task_calendars: list[TaskCalendar] = []
    case_collections: list["CaseCollection"] = []
    note_forms: list["NoteForm"] = []
    history_forms: list["HistoryForm"] = []


class NoteForm(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    form_id: int
    form: Optional[Form] = None


class HistoryForm(Form):
    user_name: str
    form_id: int
    form: Optional[Form] = None
    # make NOT optional inherited fields optional in history
    form_type_id: Optional[int] = None


class FormRequest(FormBase, BaseSchema):
    pass


class FormResponse(ResponseBase):
    forms: list[Form] = []


# case_collection
class CaseCollectionBase(StatusBase):
    quote_date: datetime
    quote_amount: condecimal(max_digits=5, decimal_places=2)
    initial_payment: condecimal(max_digits=5, decimal_places=2)
    collection_method_id: int
    court_case_id: int
    form_id: Optional[int] = None

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("case_collection").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class CaseCollection(CaseCollectionBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    collection_method: Optional[CollectionMethod] = None
    court_case: Optional[CourtCase] = None
    form: Optional["Form"] = None
    cash_collections: list["CashCollection"] = []
    note_case_collections: list["NoteCaseCollection"] = []
    history_case_collections: list["HistoryCaseCollection"] = []


class NoteCaseCollection(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    case_collection_id: int
    case_collection: Optional[CaseCollection] = None


class HistoryCaseCollection(CaseCollection):
    user_name: str
    case_collection_id: int
    case_collection: Optional[CaseCollection] = None
    # make NOT optional inherited fields optional in history
    quote_date: Optional[datetime] = None
    quote_amount: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    initial_payment: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    collection_method_id: Optional[int] = None
    court_case_id: Optional[int] = None


class CaseCollectionRequest(CaseCollectionBase, BaseSchema):
    pass


class CaseCollectionResponse(ResponseBase):
    case_collections: list[CaseCollection] = []


# cash_collection
class CashCollectionBase(StatusBase):
    collection_date: datetime
    collected_amount: condecimal(max_digits=5, decimal_places=2)
    waived_amount: condecimal(max_digits=5, decimal_places=2)
    memo: Optional[str] = None
    case_collection_id: int
    collection_method_id: int

    allow_empty_status: ClassVar[bool] = False

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is None:
            raise ValueError("Invalid status value of None")
        elif cls.allow_empty_status and v.strip() == "":
            pass
        elif v not in get_statuses().get("cash_collection").get("all"):
            raise ValueError(f"Invalid status value of: {v}")
        return v


class CashCollection(CashCollectionBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    collection_method: Optional[CollectionMethod] = None
    case_collection: Optional[CaseCollection] = None
    note_cash_collections: list["NoteCashCollection"] = []
    history_cash_collections: list["HistoryCashCollection"] = []


class NoteCashCollection(NoteBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    cash_collection_id: int
    cash_collection: Optional[CashCollection] = None


class HistoryCashCollection(CashCollection):
    user_name: str
    cash_collection_id: int
    cash_collection: Optional[CashCollection] = None
    # make NOT optional inherited fields optional in history
    collection_date: Optional[datetime] = None
    collected_amount: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    waived_amount: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    case_collection_id: Optional[int] = None
    collection_method_id: Optional[int] = None


class CashCollectionRequest(CashCollectionBase, BaseSchema):
    pass


class CashCollectionResponse(ResponseBase):
    cash_collections: list[CashCollection] = []
