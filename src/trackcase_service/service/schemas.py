from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal


class BaseModelSchema(BaseModel):
    id: Optional[int] = None
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
    forms: list["Form"] = []

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
    forms: list["Form"] = []

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
    cash_collections: list["CashCollection"] = []

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
    hearing_calendars: list["HearingCalendar"] = []

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
    task_calendars: list["TaskCalendar"] = []

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
    court_cases: list["CourtCase"] = []

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
    dhs_address: Optional[str] = None


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


# client
class ClientBase:
    name: str
    a_number: Optional[str] = None
    address: str
    phone: str
    email: Optional[str] = None
    judge_id: Optional[int] = None


class Client(ClientBase, BaseModelSchema):
    judge: Optional[Judge] = None
    court_cases: list["CourtCase"] = []

    class Config:
        orm_mode = True


class ClientRequest(ClientBase, BaseModel):
    pass


class ClientResponse(ResponseBase):
    clients: list[Client] = []


# court_case
class CourtCaseBase:
    case_type_id: int
    client_id: int


class CourtCase(CourtCaseBase, BaseModelSchema):
    case_type: Optional[CaseType] = None
    client: Optional[Client] = None
    forms: list["Form"] = []
    cash_collections: list["CashCollection"] = None
    hearing_calendars: list["HearingCalendar"] = None
    task_calendars: list["TaskCalendar"] = None

    class Config:
        orm_mode = True


class CourtCaseRequest(CourtCaseBase, BaseModel):
    pass


class CourtCaseResponse(ResponseBase):
    court_cases: list[CourtCase] = []


# hearing_calendar
class HearingCalendarBase:
    hearing_date: datetime
    hearing_type_id: int
    court_case_id: int


class HearingCalendar(HearingCalendarBase, BaseModelSchema):
    hearing_type: Optional[HearingType] = None
    court_case: Optional[CourtCase] = None
    task_calendars: list["TaskCalendar"] = []

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
    court_case_id: int
    hearing_calendar_id: Optional[int] = None


class TaskCalendar(TaskCalendarBase, BaseModelSchema):
    task_type: Optional[TaskType] = None
    court_case: Optional[CourtCase] = None
    hearing_calendar: Optional[HearingCalendar] = None
    forms: list["Form"] = []

    class Config:
        orm_mode = True


class TaskCalendarRequest(TaskCalendarBase, BaseModel):
    pass


class TaskCalendarResponse(ResponseBase):
    task_calendars: list[TaskCalendar] = []


# cash_collection
class CashCollectionBase:
    collection_date: datetime
    quote_amount: condecimal(max_digits=5, decimal_places=2)
    collected_amount: condecimal(max_digits=5, decimal_places=2)
    waived_amount = condecimal(max_digits=5, decimal_places=2)
    collection_method_id: int
    court_case_id: int
    form_id: Optional[int] = None


class CashCollection(CashCollectionBase, BaseModelSchema):
    collection_method: Optional[CollectionMethod] = None
    court_case: Optional[CourtCase] = None
    form: Optional["Form"] = None

    class Config:
        orm_mode = True


class CashCollectionRequest(CashCollectionBase, BaseModel):
    pass


class CashCollectionResponse(ResponseBase):
    cash_collections: list[CashCollection] = []


# form
class FormBase:
    form_type_id: int
    form_status_id: int
    court_case_id: int
    submit_date: Optional[datetime] = None
    receipt_date: Optional[datetime] = None
    rfe_date: Optional[datetime] = None
    rfe_submit_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None
    task_calendar_id: Optional[int] = None


class Form(FormBase, BaseModelSchema):
    form_status: Optional[FormStatus] = None
    form_type: Optional[FormType] = None
    task_calendar: Optional[TaskCalendar] = None
    court_case: Optional[CourtCase] = None
    cash_collections: list[CashCollection] = []

    class Config:
        orm_mode = True


class FormRequest(Form, BaseModel):
    pass


class FormResponse(ResponseBase):
    forms: list[Form] = []


# history_form
class HistoryFormBase:
    user_name: str
    form_id: int
    form_type_id: int
    form_status_id: int
    court_case_id: int
    submit_date: Optional[datetime] = None
    receipt_date: Optional[datetime] = None
    rfe_date: Optional[datetime] = None
    rfe_submit_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None
    task_calendar_id: Optional[int] = None


class HistoryForm(HistoryFormBase, BaseModelSchema):
    form: Optional[Form] = None
    form_status: Optional[FormStatus] = None
    form_type: Optional[FormType] = None
    task_calendar: Optional[TaskCalendar] = None
    court_case: Optional[CourtCase] = None

    class Config:
        orm_mode = True


class HistoryFormRequest(Form, BaseModel):
    pass


class HistoryFormResponse(ResponseBase):
    forms: list[HistoryForm] = []
