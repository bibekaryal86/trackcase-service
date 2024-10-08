from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, condecimal
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class SortConfig(BaseSchema):
    table: Optional[str] = None
    column: str
    direction: "SortDirection"


class FilterConfig(BaseSchema):
    table: Optional[str] = None
    column: str
    value: Union[str, int, float, datetime]
    operation: "FilterOperation"


class RequestMetadata(BaseSchema):
    schema_model_id: Optional[int] = None
    sort_config: Optional[SortConfig] = None
    filter_config: list[FilterConfig] = []
    page_number: Optional[int] = 1
    per_page: Optional[int] = 100
    is_include_deleted: Optional[bool] = False
    is_include_extra: Optional[bool] = False
    is_include_history: Optional[bool] = False


class ResponseMetadata(BaseSchema):
    total_items: int
    total_pages: int
    page_number: int
    per_page: int


class ErrorDetail(BaseSchema):
    error: Optional[str] = None


class NameDescBase(BaseSchema):
    name: str
    description: str


class AddressBase(BaseSchema):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None


class RequestBase(BaseSchema):
    pass


class ResponseBase(BaseSchema):
    delete_count: Optional[int] = None
    error: Optional[ErrorDetail] = None
    metadata: Optional[ResponseMetadata] = None


class BaseModelSchema(BaseSchema):
    id: Optional[int] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_date: Optional[datetime] = None


# component status
class ComponentStatusBase:
    component_name: str
    status_name: str
    is_active: bool


class ComponentStatus(ComponentStatusBase, BaseModelSchema):
    pass
    # do not include orm in status


class ComponentStatusRequest(ComponentStatusBase, RequestBase):
    pass


class ComponentStatusResponse(ResponseBase):
    data: list[ComponentStatus] = []


# app user role
class AppUserRoleBase:
    app_user_id: int
    app_role_id: int


class AppUserRole(AppUserRoleBase, BaseModelSchema):
    # from raw sql
    email: Optional[str] = None
    full_name: Optional[str] = None
    role_name: Optional[str] = None


class AppUserRoleRequest(AppUserRoleBase, RequestBase):
    pass


class AppUserRoleResponse(ResponseBase):
    data: list[AppUserRole] = []


# app role permission
class AppRolePermissionBase:
    app_role_id: int
    app_permission_id: int


class AppRolePermission(AppRolePermissionBase, BaseModelSchema):
    # from raw sql
    role_name: Optional[str] = None
    permission_name: Optional[str] = None


class AppRolePermissionRequest(AppRolePermissionBase, RequestBase):
    pass


class AppRolePermissionResponse(ResponseBase):
    data: list[AppRolePermission] = []


# app user
class AppUserBase(AddressBase):
    email: str
    full_name: str
    component_status_id: int
    is_validated: bool
    last_login: Optional[datetime] = None
    comments: Optional[str] = None


class AppUser(AppUserBase, BaseModelSchema):
    component_status: Optional[ComponentStatus] = None
    app_roles: list["AppRole"] = []

    def to_token(self):
        return {
            "id": self.id,
            "is_deleted": self.is_deleted,
            "email": self.email,
            "name": self.full_name,
            "status": {
                "id": self.component_status_id,
                "name": (
                    self.component_status.status_name if self.component_status else None
                ),
            },
            "roles": [
                {
                    "name": role.name,
                    "permissions": (
                        [
                            {"name": permission.name}
                            for permission in role.app_permissions
                        ]
                        if role.app_permissions
                        else []
                    ),
                }
                for role in self.app_roles
            ],
        }


class AppUserRequest(AppUserBase, RequestBase):
    # Password is required for insert, Optional for update
    password: Optional[str] = None
    is_guest_user: Optional[str] = None


class AppUserResponse(ResponseBase):
    data: list[AppUser] = []


# app user login
class AppUserLoginRequest(BaseSchema):
    username: str
    password: str


class AppUserLoginResponse(BaseSchema):
    token: str
    app_user_details: AppUser


# app role
class AppRoleBase(NameDescBase):
    pass


class AppRole(AppRoleBase, BaseModelSchema):
    app_users: list[AppUser] = []
    app_permissions: list["AppPermission"] = []


class AppRoleRequest(AppRoleBase, RequestBase):
    pass


class AppRoleResponse(ResponseBase):
    data: list[AppRole] = []


# app permission
class AppPermissionBase(NameDescBase):
    pass


class AppPermission(AppPermissionBase, BaseModelSchema):
    app_roles: list[AppRole] = []


class AppPermissionRequest(AppPermissionBase, RequestBase):
    pass


class AppPermissionResponse(ResponseBase):
    data: list[AppPermission] = []


# filing type
class FilingTypeBase(NameDescBase):
    pass


class FilingType(FilingTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    filings: list["Filing"] = []
    history_filings: list["HistoryFiling"] = []


class FilingTypeRequest(FilingTypeBase, RequestBase):
    pass


class FilingTypeResponse(ResponseBase):
    data: list[FilingType] = []


# collection method
class CollectionMethodBase(NameDescBase):
    pass


class CollectionMethod(CollectionMethodBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    cash_collections: list["CashCollection"] = []
    history_cash_collections: list["HistoryCashCollection"] = []


class CollectionMethodRequest(CollectionMethodBase, RequestBase):
    pass


class CollectionMethodResponse(ResponseBase):
    data: list[CollectionMethod] = []


# hearing type
class HearingTypeBase(NameDescBase):
    pass


class HearingType(HearingTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    hearing_calendars: list["HearingCalendar"] = []
    history_hearing_calendars: list["HistoryHearingCalendar"] = []


class HearingTypeRequest(HearingTypeBase, RequestBase):
    pass


class HearingTypeResponse(ResponseBase):
    data: list[HearingType] = []


# task type
class TaskTypeBase(NameDescBase):
    pass


class TaskType(TaskTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    task_calendars: list["TaskCalendar"] = []
    history_task_calendars: list["HistoryTaskCalendar"] = []


class TaskTypeRequest(TaskTypeBase, RequestBase):
    pass


class TaskTypeResponse(ResponseBase):
    data: list[TaskType] = []


# case type
class CaseTypeBase(NameDescBase):
    pass


class CaseType(CaseTypeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    court_cases: list["CourtCase"] = []
    history_court_cases: list["HistoryCourtCase"] = []


class CaseTypeRequest(CaseTypeBase, RequestBase):
    pass


class CaseTypeResponse(ResponseBase):
    data: list[CaseType] = []


# common ref types
class RefTypesResponseData(BaseSchema):
    component_statuses: Optional[ComponentStatusResponse] = None
    collection_methods: Optional[CollectionMethodResponse] = None
    case_types: Optional[CaseTypeResponse] = None
    filing_types: Optional[FilingTypeResponse] = None
    hearing_types: Optional[HearingTypeResponse] = None
    task_types: Optional[TaskTypeResponse] = None


class RefTypesResponse(ResponseBase):
    data: RefTypesResponseData


# court
class CourtBase(AddressBase):
    name: str
    dhs_address: Optional[str] = None
    court_url: str
    component_status_id: int
    comments: Optional[str] = None


class Court(CourtBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    judges: list["Judge"] = []
    history_courts: list["HistoryCourt"] = []
    history_judges: list["HistoryJudge"] = []


class HistoryCourt(Court):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    app_user_id: int
    court_id: int
    app_user: Optional[AppUser] = None
    court: Optional[Court] = None
    # make NOT optional inherited fields optional in history
    court_url: Optional[str] = None
    component_status_id: Optional[int] = None
    name: Optional[str] = None


class CourtRequest(CourtBase, RequestBase):
    pass


class CourtResponse(ResponseBase):
    data: list[Court] = []


# judge
class JudgeBase:
    name: str
    webex: Optional[str] = None
    court_id: int
    component_status_id: int
    comments: Optional[str] = None


class Judge(JudgeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    court: Optional[Court] = None
    clients: list["Client"] = []
    history_judges: list["HistoryJudge"] = []
    history_clients: list["HistoryClient"] = []


class HistoryJudge(Judge):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    app_user_id: int
    judge_id: int
    app_user: Optional[AppUser] = None
    judge: Optional[Judge] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None
    court_id: Optional[int] = None
    component_status_id: Optional[int] = None


class JudgeRequest(JudgeBase, RequestBase):
    pass


class JudgeResponse(ResponseBase):
    data: list[Judge] = []


# client
class ClientBase(AddressBase):
    name: str
    a_number: Optional[str] = None
    email: Optional[str] = None
    judge_id: Optional[int] = None
    component_status_id: int
    comments: Optional[str] = None


class Client(ClientBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    judge: Optional[Judge] = None
    court_cases: list["CourtCase"] = []
    history_clients: list["HistoryClient"] = []
    history_court_cases: list["HistoryCourtCase"] = []


class HistoryClient(Client):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    app_user_id: int
    client_id: int
    app_user: Optional[AppUser] = None
    client: Optional[Client] = None
    # make NOT optional inherited fields optional in history
    name: Optional[str] = None
    component_status_id: Optional[int] = None


class ClientRequest(ClientBase, RequestBase):
    pass


class ClientResponse(ResponseBase):
    data: list[Client] = []


# court_case
class CourtCaseBase:
    case_type_id: int
    client_id: int
    component_status_id: int
    comments: Optional[str] = None


class CourtCase(CourtCaseBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    case_type: Optional[CaseType] = None
    client: Optional[Client] = None
    filings: list["Filing"] = []
    case_collections: list["CaseCollection"] = []
    hearing_calendars: list["HearingCalendar"] = []
    history_court_cases: list["HistoryCourtCase"] = []
    history_hearing_calendars: list["HistoryHearingCalendar"] = []
    history_filings: list["HistoryFiling"] = []
    history_case_collections: list["HistoryCaseCollection"] = []


class HistoryCourtCase(CourtCase):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    app_user_id: int
    court_case_id: int
    app_user: Optional[AppUser] = None
    court_case: Optional[CourtCase] = None
    # make NOT optional inherited fields optional in history
    case_type_id: Optional[int] = None
    client_id: Optional[int] = None
    component_status_id: Optional[int] = None


class CourtCaseRequest(CourtCaseBase, RequestBase):
    pass


class CourtCaseResponse(ResponseBase):
    data: list[CourtCase] = []


# hearing_calendar
class HearingCalendarBase:
    hearing_date: datetime
    hearing_type_id: int
    court_case_id: int
    component_status_id: int
    comments: Optional[str] = None


class HearingCalendar(HearingCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    hearing_type: Optional[HearingType] = None
    court_case: Optional[CourtCase] = None
    task_calendars: list["TaskCalendar"] = []
    history_hearing_calendars: list["HistoryHearingCalendar"] = []
    history_task_calendars: list["HistoryTaskCalendar"] = []


class HistoryHearingCalendar(HearingCalendar):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    app_user_id: int
    hearing_calendar_id: int
    app_user: Optional[AppUser] = None
    hearing_calendar: Optional[HearingCalendar] = None
    # make NOT optional inherited fields optional in history
    hearing_date: Optional[datetime] = None
    hearing_type_id: Optional[int] = None
    court_case_id: Optional[int] = None


class HearingCalendarRequest(HearingCalendarBase, RequestBase):
    pass


class HearingCalendarResponse(ResponseBase):
    data: list[HearingCalendar] = []


# task_calendar
class TaskCalendarBase:
    task_date: datetime
    due_date: datetime
    task_type_id: int
    hearing_calendar_id: Optional[int] = None
    filing_id: Optional[int] = None
    component_status_id: int
    comments: Optional[str] = None


class TaskCalendar(TaskCalendarBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    task_type: Optional[TaskType] = None
    hearing_calendar: Optional[HearingCalendar] = None
    filing: Optional["Filing"] = None
    history_task_calendars: list["HistoryTaskCalendar"] = []


class HistoryTaskCalendar(TaskCalendar):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    app_user_id: int
    task_calendar_id: int
    app_user: Optional[AppUser] = None
    task_calendar: Optional[TaskCalendar] = None
    # make NOT optional inherited fields optional in history
    task_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    task_type_id: Optional[int] = None
    component_status_id: Optional[int] = None


class TaskCalendarRequest(TaskCalendarBase, RequestBase):
    pass


class TaskCalendarResponse(ResponseBase):
    data: list[TaskCalendar] = []


# common calendars
class CalendarEvent(BaseSchema):
    id: int
    calendar: str
    type: str
    date: datetime
    status: str
    title: str
    court_case_id: int


class CalendarResponseData(BaseSchema):
    calendar_events: list[CalendarEvent] = []
    hearing_calendars: list[HearingCalendar] = []
    task_calendars: list[TaskCalendar] = []


class CalendarResponse(ResponseBase):
    data: CalendarResponseData


# filing
class FilingBase:
    filing_type_id: int
    court_case_id: int
    submit_date: Optional[datetime] = None
    receipt_date: Optional[datetime] = None
    receipt_number: Optional[str] = None
    priority_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None
    component_status_id: int
    comments: Optional[str] = None


class Filing(FilingBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    filing_type: Optional[FilingType] = None
    court_case: Optional[CourtCase] = None
    filing_rfes: list["FilingRfe"] = []
    task_calendars: list[TaskCalendar] = []
    history_filings: list["HistoryFiling"] = []
    history_filing_rfes: list["HistoryFilingRfe"] = []
    history_task_calendars: list[HistoryTaskCalendar] = []


class HistoryFiling(Filing):
    app_user_id: int
    filing_id: int
    app_user: Optional[AppUser] = None
    filing: Optional[Filing] = None
    # make NOT optional inherited fields optional in history
    filing_type_id: Optional[int] = None
    component_status_id: Optional[int] = None


class FilingRequest(FilingBase, RequestBase):
    pass


class FilingResponse(ResponseBase):
    data: list[Filing] = []


# filing
class FilingRfeBase:
    filing_id: int
    rfe_date: datetime
    rfe_submit_date: Optional[datetime] = None
    rfe_reason: str
    comments: Optional[str] = None


class FilingRfe(FilingRfeBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    filing: Optional[Filing] = None
    history_filing_rfes: list["HistoryFilingRfe"] = []


class HistoryFilingRfe(FilingRfe):
    app_user_id: int
    filing_rfe_id: int
    app_user: Optional[AppUser] = None
    filing_rfe: Optional[FilingRfe] = None
    filing: Optional[Filing] = None
    # make NOT optional inherited fields optional in history
    filing_id: Optional[int] = None
    rfe_date: Optional[datetime] = None
    rfe_reason: Optional[str] = None


class FilingRfeRequest(FilingRfeBase, RequestBase):
    pass


class FilingRfeResponse(ResponseBase):
    data: list[FilingRfe] = []


# case_collection
class CaseCollectionBase:
    quote_amount: condecimal(max_digits=7, decimal_places=2)
    court_case_id: int
    component_status_id: int
    comments: Optional[str] = None


class CaseCollection(CaseCollectionBase, BaseModelSchema):
    balance_amount: Optional[condecimal(max_digits=7, decimal_places=2)] = None
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    component_status: Optional[ComponentStatus] = None
    court_case: Optional[CourtCase] = None
    cash_collections: list["CashCollection"] = []
    history_case_collections: list["HistoryCaseCollection"] = []
    history_cash_collections: list["HistoryCashCollection"] = []


class HistoryCaseCollection(CaseCollection):
    app_user_id: int
    case_collection_id: int
    app_user: Optional[AppUser] = None
    case_collection: Optional[CaseCollection] = None
    # make NOT optional inherited fields optional in history
    quote_amount: Optional[condecimal(max_digits=7, decimal_places=2)] = None
    court_case_id: Optional[int] = None
    component_status_id: Optional[int] = None


class CaseCollectionRequest(CaseCollectionBase, RequestBase):
    pass


class CaseCollectionResponse(ResponseBase):
    data: list[CaseCollection] = []


# cash_collection
class CashCollectionBase:
    collection_date: datetime
    collected_amount: condecimal(max_digits=7, decimal_places=2)
    waived_amount: condecimal(max_digits=7, decimal_places=2)
    memo: str
    case_collection_id: int
    collection_method_id: int


class CashCollection(CashCollectionBase, BaseModelSchema):
    # model_config = ConfigDict(from_attributes=True, extra="ignore")
    collection_method: Optional[CollectionMethod] = None
    case_collection: Optional[CaseCollection] = None
    history_cash_collections: list["HistoryCashCollection"] = []


class HistoryCashCollection(CashCollection):
    app_user_id: int
    cash_collection_id: int
    app_user: Optional[AppUser] = None
    cash_collection: Optional[CashCollection] = None
    # make NOT optional inherited fields optional in history
    collection_date: Optional[datetime] = None
    collected_amount: Optional[condecimal(max_digits=7, decimal_places=2)] = None
    waived_amount: Optional[condecimal(max_digits=7, decimal_places=2)] = None
    case_collection_id: Optional[int] = None
    collection_method_id: Optional[int] = None


class CashCollectionRequest(CashCollectionBase, RequestBase):
    pass


class CashCollectionResponse(ResponseBase):
    data: list[CashCollection] = []


# enums
class LogLevelOptions(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


class CalendarObjectTypes(str, Enum):
    HEARING = "HEARING_CALENDAR"
    TASK = "TASK_CALENDAR"


class SortDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class FilterOperation(str, Enum):
    EQUAL_TO = "eq"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    GREATER_THAN_OR_EQUAL_TO = "gte"
    LESS_THAN_OR_EQUAL_TO = "lte"


class UserManagementServiceRegistry(str, Enum):
    APP_USER = "APP_USER"
    APP_ROLE = "APP_ROLE"
    APP_PERMISSION = "APP_PERMISSION"
    APP_USER_ROLE = "APP_USER_ROLE"
    APP_ROLE_PERMISSION = "APP_ROLE_PERMISSION"
    APP_USER_ROLE_PERMISSION = "APP_USER_ROLE_PERMISSION"


class RefTypesServiceRegistry(str, Enum):
    COMPONENT_STATUS = "COMPONENT_STATUS"
    COLLECTION_METHOD = "COLLECTION_METHOD"
    CASE_TYPE = "CASE_TYPE"
    FILING_TYPE = "FILING_TYPE"
    HEARING_TYPE = "HEARING_TYPE"
    TASK_TYPE = "TASK_TYPE"


class CalendarServiceRegistry(str, Enum):
    HEARING_CALENDAR = "HEARING_CALENDAR"
    TASK_CALENDAR = "TASK_CALENDAR"


class CollectionServiceRegistry(str, Enum):
    CASE_COLLECTION = "CASE_COLLECTION"
    CASH_COLLECTION = "CASH_COLLECTION"


class ComponentStatusNames(str, Enum):
    APP_USERS = "APP_USERS"
    COURTS = "COURTS"
    JUDGES = "JUDGES"
    CLIENTS = "CLIENTS"
    COURT_CASES = "COURT_CASES"
    CALENDARS = "CALENDARS"
    FILINGS = "FILINGS"
    COLLECTIONS = "COLLECTIONS"


class ComponentStatusTypes(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ALL = "ALL"
