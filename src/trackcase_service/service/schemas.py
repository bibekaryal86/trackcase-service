from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal


class BaseModelSchema(BaseModel):
    id: Optional[int] = 0
    created: Optional[datetime] = None
    modified: Optional[datetime] = None


class ResponseBase(BaseModel):
    delete_count: Optional[int] = 0
    msg: Optional[str] = None
    err_msg: Optional[str] = None


class NameDescBase:
    name: str
    description: str


# form type
class FormTypeBase(NameDescBase):
    pass


class FormType(FormTypeBase, BaseModelSchema):
    forms: Optional["Form"] = []

    class Config:
        orm_mode = True


class FormTypeRequest(FormTypeBase, BaseModel):
    pass


class FormTypeResponse(ResponseBase):
    form_types: list[FormType] = []


# form status
class FormStatusBase(NameDescBase):
    pass


class FormStatus(FormStatusBase, BaseModelSchema):
    forms: Optional["Form"] = []

    class Config:
        orm_mode = True


class FormStatusRequest(FormStatusBase, BaseModel):
    pass


class FormStatusResponse(ResponseBase):
    form_statuses: list[FormStatus] = []


# collection method
class CollectionMethodBase(NameDescBase):
    pass


class CollectionMethod(CollectionMethodBase, BaseModelSchema):
    cash_collections: Optional["CashCollection"] = []

    class Config:
        orm_mode = True


class CollectionMethodRequest(CollectionMethodBase, BaseModel):
    pass


class CollectionMethodResponse(ResponseBase):
    collection_methods: list[CollectionMethod] = []


# hearing type
class HearingTypeBase(NameDescBase):
    pass


class HearingType(HearingTypeBase, BaseModelSchema):
    hearing_calendars: Optional["HearingCalendar"] = []

    class Config:
        orm_mode = True


class HearingTypeRequest(HearingTypeBase, BaseModel):
    pass


class HearingTypeResponse(ResponseBase):
    hearing_types: list[HearingType] = []


# task type
class TaskTypeBase(NameDescBase):
    pass


class TaskType(TaskTypeBase, BaseModelSchema):
    task_calendars: Optional["TaskCalendar"] = []

    class Config:
        orm_mode = True


class TaskTypeRequest(TaskTypeBase, BaseModel):
    pass


class TaskTypeResponse(ResponseBase):
    task_types: list[TaskType] = []


# case type
class CaseTypeBase(NameDescBase):
    pass


class CaseType(CaseTypeBase, BaseModelSchema):
    court_cases: Optional[list["CourtCase"]] = []

    class Config:
        orm_mode = True


class CaseTypeRequest(CaseTypeBase, BaseModel):
    pass


class CaseTypeResponse(ResponseBase):
    case_types: list[CaseType] = []


# court
class CourtBase:
    name: str
    address: str
    dhs_address: str


class Court(CourtBase, BaseModelSchema):
    judges: list["Judge"] = []

    class Config:
        orm_mode = True


class CourtRequest(CourtBase, BaseModel):
    pass


class CourtResponse(ResponseBase):
    courts: list[Court] = []


# judge
class JudgeBase:
    name: str
    webex: Optional[str] = None
    court_id: int


class Judge(JudgeBase, BaseModelSchema):
    court: Optional[Court] = None
    clients: list["Client"] = []

    class Config:
        orm_mode = True


class JudgeRequest(JudgeBase, BaseModel):
    pass


class JudgeResponse(ResponseBase):
    judges: list[Judge] = []


# form
class FormBase:
    submit_date: datetime
    form_status_id: int
    form_type_id: int
    receipt_date: Optional[datetime] = None
    rfe_date: Optional[datetime] = None
    rfe_submit_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None


class Form(FormBase, BaseModelSchema):
    form_status: Optional[FormStatus] = None
    form_type: Optional[FormType] = None
    task_calendar_forms: list["TaskCalendarForm"] = []
    court_case_forms: list["CourtCaseForm"] = []

    class Config:
        orm_mode = True


class FormRequest(Form, BaseModel):
    pass


class FormResponse(ResponseBase):
    forms: list[Form] = []


# client
class ClientBase:
    name: str
    a_number: str
    address: str
    phone: str
    email: Optional[str] = None
    judge_id: Optional[int] = None


class Client(ClientBase, BaseModelSchema):
    judge: Optional[Judge] = None
    court_cases: Optional["CourtCase"] = None

    class Config:
        orm_mode = True


class ClientRequest(ClientBase, BaseModel):
    pass


class ClientResponse(ResponseBase):
    clients: list[Client] = []


# cash_collection
class CashCollectionBase:
    collection_date: datetime
    quote_amount: condecimal(max_digits=6, decimal_places=2)
    collected_amount: condecimal(max_digits=6, decimal_places=2)
    collection_method_id: int


class CashCollection(CashCollectionBase, BaseModelSchema):
    collection_method: Optional[CollectionMethod] = None
    court_case_cash_collections: list["CourtCaseCashCollection"] = []

    class Config:
        orm_mode = True


class CashCollectionRequest(CashCollectionBase, BaseModel):
    pass


class CashCollectionResponse(ResponseBase):
    cash_collections: list[CashCollection] = []


# hearing_calendar
class HearingCalendarBase:
    hearing_date: datetime
    hearing_type_id: int


class HearingCalendar(HearingCalendarBase, BaseModelSchema):
    hearing_type: Optional[HearingType] = None
    task_calendars: list["TaskCalendar"] = []
    court_case_hearing_calendars: list["CourtCaseHearingCalendar"] = []

    class Config:
        orm_mode = True


class HearingCalendarRequest(HearingCalendarBase, BaseModel):
    pass


class HearingCalendarResponse(ResponseBase):
    hearing_calendars: list[HearingCalendar] = []


# task_calendar
class TaskCalendarBase:
    task_date: datetime
    task_type_id: int
    hearing_calendar_id: Optional[int] = None


class TaskCalendar(TaskCalendarBase, BaseModelSchema):
    task_type: Optional[TaskType] = None
    hearing_calendar: Optional[HearingCalendar] = None
    task_calendar_forms: list["TaskCalendarForm"] = []
    court_case_task_calendars: list["CourtCaseTaskCalendar"] = []

    class Config:
        orm_mode = True


class TaskCalendarRequest(TaskCalendarBase, BaseModel):
    pass


class TaskCalendarResponse(ResponseBase):
    task_calendars: list[TaskCalendar] = []


# task_calendar_form
class TaskCalendarFormBase:
    form_id: int
    task_type_id: int
    hearing_calendar_id: Optional[int] = None


class TaskCalendarForm(TaskCalendarBase, BaseModelSchema):
    form: Optional[Form] = None
    task_calendar: Optional[TaskCalendar] = None

    class Config:
        orm_mode = True


class TaskCalendarFormRequest(TaskCalendarFormBase, BaseModel):
    pass


class TaskCalendarFormResponse(ResponseBase):
    task_calendar_forms: list[TaskCalendarForm] = []


# court_case
class CourtCaseBase:
    case_type_id: int
    client_id: int


class CourtCase(CourtCaseBase, BaseModelSchema):
    case_type: Optional[CaseType] = None
    client: Optional[Client] = None
    court_case_forms: list["CourtCaseForm"] = []
    court_case_cash_collections: list["CourtCaseCashCollection"] = None
    court_case_task_calendars: list["CourtCaseTaskCalendar"] = None
    court_case_hearing_calendars: list["CourtCaseHearingCalendar"] = None

    class Config:
        orm_mode = True


class CourtCaseRequest(CourtCaseBase, BaseModel):
    pass


class CourtCaseResponse(ResponseBase):
    court_cases: list[CourtCase] = []


# court_case_form
class CourtCaseFormBase:
    case_id: int
    form_id: int


class CourtCaseForm(CourtCaseFormBase, BaseModelSchema):
    court_case: Optional[CourtCase] = None
    form: Optional[Form] = None

    class Config:
        orm_mode = True


class CourtCaseFormRequest(CourtCaseFormBase, BaseModel):
    pass


class CourtCaseFormResponse(ResponseBase):
    court_case_forms: list[CourtCaseForm] = []


# court_case_cash_collection
class CourtCaseCashCollectionBase:
    case_id: int
    cash_collection_id: int


class CourtCaseCashCollection(CourtCaseCashCollectionBase, BaseModelSchema):
    court_case: Optional[CourtCase] = None
    cash_collection: Optional[CashCollection] = None

    class Config:
        orm_mode = True


class CourtCaseCashCollectionRequest(CourtCaseCashCollectionBase, BaseModel):
    pass


class CourtCaseCashCollectionResponse(ResponseBase):
    court_case_cash_collections: list[CourtCaseCashCollection] = []


# court_case_task_calendar
class CourtCaseTaskCalendarBase:
    case_id: int
    task_calendar_id: int


class CourtCaseTaskCalendar(CourtCaseTaskCalendarBase, BaseModelSchema):
    court_case: Optional[CourtCase] = None
    task_calendar: Optional[TaskCalendar] = None

    class Config:
        orm_mode = True


class CourtCaseTaskCalendarRequest(CourtCaseTaskCalendarBase, BaseModel):
    pass


class CourtCaseTaskCalendarResponse(ResponseBase):
    court_case_task_calendars: list[CourtCaseTaskCalendar] = []


# court_case_hearing_calendar
class CourtCaseHearingCalendarBase:
    case_id: int
    hearing_calendar_id: int


class CourtCaseHearingCalendar(CourtCaseHearingCalendarBase, BaseModelSchema):
    court_case: Optional[CourtCase] = None
    hearing_calendar: Optional[HearingCalendar] = None

    class Config:
        orm_mode = True


class CourtCaseHearingCalendarRequest(CourtCaseHearingCalendarBase, BaseModel):
    pass


class CourtCaseHearingCalendarResponse(ResponseBase):
    court_case_hearing_calendars: list[CourtCaseHearingCalendar] = []
