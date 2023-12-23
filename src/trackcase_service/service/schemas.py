from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal, field_validator

from src.trackcase_service.utils.constants import get_statuses


class BaseModelSchema(BaseModel):
    id: Optional[int] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None


class ErrorDetail(BaseModel):
    error: Optional[str] = None


class ResponseBase(BaseModel):
    delete_count: Optional[int] = 0
    detail: Optional[ErrorDetail] = None


class NameDescBase:
    name: str
    description: str


class StatusBase(BaseModel):
    status: str
    comments: Optional[str] = None


class AddressBase(BaseModel):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[int] = None


class NoteBase(BaseModel):
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
    history_forms: list["HistoryForm"] = []


class FormTypeRequest(FormTypeBase, BaseModel):
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
    history_cash_collections: list["HistoryCashCollection"] = []
    history_case_collections: list["HistoryCaseCollection"] = []


class CollectionMethodRequest(CollectionMethodBase, BaseModel):
    pass


class CollectionMethodResponse(ResponseBase):
    collection_methods: list[CollectionMethod] = []


# hearing type
class HearingTypeBase(NameDescBase):
    pass


class HearingType(HearingTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    hearing_calendars: list["HearingCalendar"] = []
    history_hearing_calendars: list["HistoryHearingCalendar"] = []


class HearingTypeRequest(HearingTypeBase, BaseModel):
    pass


class HearingTypeResponse(ResponseBase):
    hearing_types: list[HearingType] = []


# task type
class TaskTypeBase(NameDescBase):
    pass


class TaskType(TaskTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    task_calendars: list["TaskCalendar"] = []
    history_task_calendars: list["HistoryTaskCalendar"] = []


class TaskTypeRequest(TaskTypeBase, BaseModel):
    pass


class TaskTypeResponse(ResponseBase):
    task_types: list[TaskType] = []


# case type
class CaseTypeBase(NameDescBase):
    pass


class CaseType(CaseTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court_cases: list["CourtCase"] = []
    history_court_cases: list["HistoryCourtCase"] = []


class CaseTypeRequest(CaseTypeBase, BaseModel):
    pass


class CaseTypeResponse(ResponseBase):
    case_types: list[CaseType] = []


# court
class CourtBase(AddressBase, StatusBase):
    name: str
    dhs_address: Optional[str] = None

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("court", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class Court(CourtBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    judges: list["Judge"] = []
    note_courts: list["NoteCourt"] = []
    history_courts: list["HistoryCourt"] = []
    history_judges: list["HistoryJudge"] = []


class NoteCourtBase(NoteBase):
    court_id: int


class NoteCourt(NoteCourtBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court: Optional[Court] = None


class HistoryCourt(Court):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    court_id: int
    court: Optional[Court] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None


class CourtRequest(CourtBase, BaseModel):
    pass


class CourtResponse(ResponseBase):
    courts: list[Court] = []


class NoteCourtRequest(NoteCourtBase, BaseModel):
    pass


class NoteCourtResponse(ResponseBase):
    note_courts: list[NoteCourt] = []


# judge
class JudgeBase(StatusBase):
    name: str
    webex: Optional[str] = None
    court_id: int

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("judge", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class Judge(JudgeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court: Optional[Court] = None
    clients: list["Client"] = []
    note_judges: list["NoteJudge"] = []
    history_judges: list["HistoryJudge"] = []
    history_clients: list["HistoryClient"] = []


class NoteJudgeBase(NoteBase):
    judge_id: int


class NoteJudge(NoteJudgeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    judge: Optional[Judge] = None


class HistoryJudge(Judge):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    judge_id: int
    judge: Optional[Judge] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None
    court_id: Optional[int] = None


class JudgeRequest(JudgeBase, BaseModel):
    pass


class JudgeResponse(ResponseBase):
    judges: list[Judge] = []


class NoteJudgeRequest(NoteJudgeBase, BaseModel):
    pass


class NoteJudgeResponse(ResponseBase):
    note_judges: list[NoteJudge] = []


# client
class ClientBase(AddressBase, StatusBase):
    name: str
    a_number: Optional[str] = None
    phone: str
    email: Optional[str] = None
    judge_id: Optional[int] = None

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("client", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class Client(ClientBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    judge: Optional[Judge] = None
    court_cases: list["CourtCase"] = []
    note_clients: list["NoteClient"] = []
    history_clients: list["HistoryClient"] = []
    history_court_cases: list["HistoryCourtCase"] = []


class NoteClientBase(NoteBase):
    client_id: int


class NoteClient(NoteClientBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    client: Optional[Client] = None


class HistoryClient(Client):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    client_id: int
    client: Optional[Client] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None
    phone: Optional[str] = None


class ClientRequest(ClientBase, BaseModel):
    pass


class ClientResponse(ResponseBase):
    clients: list[Client] = []


class NoteClientRequest(NoteClientBase, BaseModel):
    pass


class NoteClientResponse(ResponseBase):
    note_clients: list[NoteClient] = []


# court_case
class CourtCaseBase(StatusBase):
    case_type_id: int
    client_id: int

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("court_case", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class CourtCase(CourtCaseBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    case_type: Optional[CaseType] = None
    client: Optional[Client] = None
    forms: list["Form"] = []
    case_collections: list["CaseCollection"] = []
    hearing_calendars: list["HearingCalendar"] = []
    task_calendars: list["TaskCalendar"] = []
    note_court_cases: list["NoteCourtCase"] = []
    history_court_cases: list["HistoryCourtCase"] = []
    history_hearing_calendars: list["HistoryHearingCalendar"] = []
    history_task_calendars: list["HistoryTaskCalendar"] = []
    history_forms: list["HistoryForm"] = []
    history_case_collections: list["HistoryCaseCollection"] = []


class NoteCourtCaseBase(NoteBase):
    court_case_id: int


class NoteCourtCase(NoteCourtCaseBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court_case: Optional[CourtCase] = None


class HistoryCourtCase(CourtCase):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    court_case_id: int
    court_case: Optional[CourtCase] = None
    # make NOT optional inherited fields optional in history
    case_type_id: Optional[int] = None
    client_id: Optional[int] = None


class CourtCaseRequest(CourtCaseBase, BaseModel):
    pass


class CourtCaseResponse(ResponseBase):
    court_cases: list[CourtCase] = []


class NoteCourtCaseRequest(NoteCourtCaseBase, BaseModel):
    pass


class NoteCourtCaseResponse(ResponseBase):
    note_court_cases: list[NoteCourtCase] = []


# hearing_calendar
class HearingCalendarBase(StatusBase):
    hearing_date: datetime
    hearing_type_id: int
    court_case_id: int

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("hearing_calendar", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class HearingCalendar(HearingCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    hearing_type: Optional[HearingType] = None
    court_case: Optional[CourtCase] = None
    task_calendars: list["TaskCalendar"] = []
    note_hearing_calendars: list["NoteHearingCalendar"] = []
    history_hearing_calendars: list["HistoryHearingCalendar"] = []
    history_task_calendars: list["HistoryTaskCalendar"] = []


class NoteHearingCalendarBase(NoteBase):
    hearing_calendar_id: int


class NoteHearingCalendar(NoteHearingCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
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


class HearingCalendarRequest(HearingCalendarBase, BaseModel):
    pass


class HearingCalendarResponse(ResponseBase):
    hearing_calendars: list[HearingCalendar] = []


class NoteHearingCalendarRequest(NoteHearingCalendarBase, BaseModel):
    pass


class NoteHearingCalendarResponse(ResponseBase):
    note_hearing_calendars: list[NoteHearingCalendar] = []


# task_calendar
class TaskCalendarBase(StatusBase):
    task_date: datetime
    task_type_id: int
    court_case_id: int
    hearing_calendar_id: Optional[int] = None

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("task_calendar", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class TaskCalendar(TaskCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    task_type: Optional[TaskType] = None
    court_case: Optional[CourtCase] = None
    hearing_calendar: Optional[HearingCalendar] = None
    forms: list["Form"] = []
    note_task_calendars: list["NoteTaskCalendar"] = []
    history_task_calendars: list["HistoryTaskCalendar"] = []
    history_forms: list["HistoryForm"] = []


class NoteTaskCalendarBase(NoteBase):
    hearing_calendar_id: int


class NoteTaskCalendar(NoteTaskCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    task_calendar: Optional[TaskCalendar] = None


class HistoryTaskCalendar(TaskCalendar):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    user_name: str
    task_calendar_id: int
    task_calendar: Optional[TaskCalendar] = None
    # make NOT optional inherited fields optional in history
    task_date: Optional[datetime] = None
    task_type_id: Optional[int] = None
    court_case_id: Optional[int] = None


class TaskCalendarRequest(TaskCalendarBase, BaseModel):
    pass


class TaskCalendarResponse(ResponseBase):
    task_calendars: list[TaskCalendar] = []


class NoteTaskCalendarRequest(NoteTaskCalendarBase, BaseModel):
    pass


class NoteTaskCalendarResponse(ResponseBase):
    note_task_calendars: list[NoteTaskCalendar] = []


# form
class FormBase(StatusBase):
    form_type_id: int
    court_case_id: Optional[int] = None
    submit_date: Optional[datetime] = None
    receipt_date: Optional[datetime] = None
    rfe_date: Optional[datetime] = None
    rfe_submit_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None
    task_calendar_id: Optional[int] = None

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("form", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class Form(FormBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    form_type: Optional[FormType] = None
    task_calendar: Optional[TaskCalendar] = None
    court_case: Optional[CourtCase] = None
    case_collections: list["CaseCollection"] = []
    note_forms: list["NoteForm"] = []
    history_forms: list["HistoryForm"] = []
    history_case_collections: list["HistoryCaseCollection"] = []


class NoteFormBase(NoteBase):
    form_id: int


class NoteForm(NoteFormBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    form: Optional[Form] = None


class HistoryForm(Form):
    user_name: str
    form_id: int
    form: Optional[Form] = None
    # make NOT optional inherited fields optional in history
    form_type_id: Optional[int] = None


class FormRequest(FormBase, BaseModel):
    pass


class FormResponse(ResponseBase):
    forms: list[Form] = []


class NoteFormRequest(NoteFormBase, BaseModel):
    pass


class NoteFormResponse(ResponseBase):
    note_forms: list[NoteForm] = []


# case_collection
class CaseCollectionBase(StatusBase):
    quote_date: datetime
    quote_amount: condecimal(max_digits=5, decimal_places=2)
    initial_payment: condecimal(max_digits=5, decimal_places=2)
    collection_method_id: int
    court_case_id: int
    form_id: Optional[int] = None

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("case_collection", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class CaseCollection(CaseCollectionBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    collection_method: Optional[CollectionMethod] = None
    court_case: Optional[CourtCase] = None
    form: Optional["Form"] = None
    cash_collections: list["CashCollection"] = []
    note_case_collections: list["NoteCaseCollection"] = []
    history_case_collections: list["HistoryCaseCollection"] = []
    history_cash_collections: list["HistoryCashCollection"] = []


class NoteCaseCollectionBase(NoteBase):
    case_collection_id: int


class NoteCaseCollection(NoteCaseCollectionBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
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


class CaseCollectionRequest(CaseCollectionBase, BaseModel):
    pass


class CaseCollectionRetrieveRequest(BaseModel):
    collection_method_id: Optional[int] = None
    court_case_id: Optional[int] = None
    form_id: Optional[int] = None

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if value is not None}


class CaseCollectionResponse(ResponseBase):
    case_collections: list[CaseCollection] = []


class NoteCaseCollectionRequest(NoteCaseCollectionBase, BaseModel):
    pass


class NoteCaseCollectionResponse(ResponseBase):
    note_case_collections: list[NoteCaseCollection] = []


# cash_collection
class CashCollectionBase(StatusBase):
    collection_date: datetime
    collected_amount: condecimal(max_digits=5, decimal_places=2)
    waived_amount: condecimal(max_digits=5, decimal_places=2)
    memo: Optional[str] = None
    case_collection_id: int
    collection_method_id: int

    @field_validator("status")
    @classmethod
    def check_status(cls, v: str) -> str | None:
        if v is not None and v not in get_statuses().get("cash_collection", []):
            raise ValueError(f"Invalid status value: {v}")
        return v


class CashCollection(CashCollectionBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    collection_method: Optional[CollectionMethod] = None
    case_collection: Optional[CaseCollection] = None
    note_cash_collections: list["NoteCashCollection"] = []
    history_cash_collections: list["HistoryCashCollection"] = []


class NoteCashCollectionBase(NoteBase):
    cash_collection_id: int


class NoteCashCollection(NoteCashCollectionBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
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


class CashCollectionRequest(CashCollectionBase, BaseModel):
    pass


class CashCollectionResponse(ResponseBase):
    cash_collections: list[CashCollection] = []


class NoteCashCollectionRequest(NoteCashCollectionBase, BaseModel):
    pass


class NoteCashCollectionResponse(ResponseBase):
    note_cash_collections: list[NoteCashCollection] = []
