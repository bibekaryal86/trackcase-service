from typing import Any, List

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

Base: Any = declarative_base()


class TableBase:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_date = Column(DateTime, nullable=True)


class NameDescBase:
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(3000), nullable=False)


class AddressBase:
    street_address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(10), nullable=True)
    zip_code = Column(String(10), nullable=True)
    phone_number = Column(String(25), nullable=True)


class ComponentStatus(TableBase, Base):
    __tablename__ = "component_status"
    component_name = Column(String(100), nullable=False)
    status_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False)

    app_users: Mapped[List["AppUser"]] = relationship("AppUser")
    courts: Mapped[List["Court"]] = relationship("Court")
    history_courts: Mapped[List["HistoryCourt"]] = relationship("HistoryCourt")
    judges: Mapped[List["Court"]] = relationship("Judge")
    history_judges: Mapped[List["HistoryCourt"]] = relationship("HistoryJudge")
    clients: Mapped[List["Client"]] = relationship("Client")
    history_clients: Mapped[List["HistoryClient"]] = relationship("HistoryClient")
    court_cases: Mapped[List["CourtCase"]] = relationship("CourtCase")
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        "HistoryCourtCase"
    )
    filings: Mapped[List["Filing"]] = relationship("Filing")
    history_filings: Mapped[List["HistoryFiling"]] = relationship("HistoryFiling")
    hearing_calendars: Mapped[List["HearingCalendar"]] = relationship("HearingCalendar")
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        "HistoryHearingCalendar"
    )
    task_calendars: Mapped[List["TaskCalendar"]] = relationship("TaskCalendar")
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        "HistoryTaskCalendar"
    )
    case_collections: Mapped[List["CaseCollection"]] = relationship("CaseCollection")
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        "HistoryCaseCollection"
    )

    __table_args__ = (
        UniqueConstraint(
            "component_name",
            "status_name",
            name="component_status_component_status_id",
        ),
    )


class AppUserRole(TableBase, Base):
    __tablename__ = "app_user_role"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="app_user_role_app_user_id",
        ),
        nullable=False,
    )
    app_role_id = Column(
        ForeignKey(
            "app_role.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="app_user_role_app_role_id",
        ),
        nullable=False,
    )


class AppRolePermission(TableBase, Base):
    __tablename__ = "app_role_permission"
    app_role_id = Column(
        ForeignKey(
            "app_role.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="app_role_permission_app_role_id",
        ),
        nullable=False,
    )
    app_permission_id = Column(
        ForeignKey(
            "app_permission.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="app_role_permission_app_permission_id",
        ),
        nullable=False,
    )


class AppUser(TableBase, AddressBase, Base):
    __tablename__ = "app_user"
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    full_name = Column(String(250), nullable=False)
    is_validated = Column(Boolean, nullable=False)
    last_login = Column(DateTime, nullable=True)
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="app_user_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(back_populates="app_users")
    app_roles: Mapped[List["AppRole"]] = relationship(
        "AppRole", secondary=AppUserRole.__tablename__, back_populates="app_users"
    )
    history_courts: Mapped[List["HistoryCourt"]] = relationship("HistoryCourt")
    history_judges: Mapped[List["HistoryCourt"]] = relationship("HistoryJudge")
    history_clients: Mapped[List["HistoryClient"]] = relationship("HistoryClient")
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        "HistoryCourtCase"
    )
    history_filings: Mapped[List["HistoryFiling"]] = relationship("HistoryFiling")
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        "HistoryHearingCalendar"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        "HistoryTaskCalendar"
    )
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        "HistoryCaseCollection"
    )
    history_cash_collections: Mapped[List["HistoryCashCollection"]] = relationship(
        "HistoryCashCollection"
    )


class AppRole(TableBase, NameDescBase, Base):
    __tablename__ = "app_role"
    app_users: Mapped[List[AppUser]] = relationship(
        "AppUser", secondary=AppUserRole.__tablename__, back_populates="app_roles"
    )
    app_permissions: Mapped[List["AppPermission"]] = relationship(
        "AppPermission",
        secondary=AppRolePermission.__tablename__,
        back_populates="app_roles",
    )


class AppPermission(TableBase, NameDescBase, Base):
    __tablename__ = "app_permission"
    app_roles: Mapped[List[AppRole]] = relationship(
        "AppRole",
        secondary=AppRolePermission.__tablename__,
        back_populates="app_permissions",
    )


class FilingType(TableBase, NameDescBase, Base):
    __tablename__ = "filing_type"
    filings: Mapped[List["Filing"]] = relationship(back_populates="filing_type")
    history_filings: Mapped[List["HistoryFiling"]] = relationship("HistoryFiling")


class CollectionMethod(TableBase, NameDescBase, Base):
    __tablename__ = "collection_method"
    cash_collections: Mapped[List["CashCollection"]] = relationship(
        back_populates="collection_method"
    )
    history_cash_collections: Mapped[List["HistoryCashCollection"]] = relationship(
        "HistoryCashCollection"
    )


class HearingType(TableBase, NameDescBase, Base):
    __tablename__ = "hearing_type"
    hearing_calendars: Mapped[List["HearingCalendar"]] = relationship(
        back_populates="hearing_type"
    )
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        "HistoryHearingCalendar"
    )


class TaskType(TableBase, NameDescBase, Base):
    __tablename__ = "task_type"
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(
        back_populates="task_type"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        "HistoryTaskCalendar"
    )


class CaseType(TableBase, NameDescBase, Base):
    __tablename__ = "case_type"
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="case_type")
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        "HistoryCourtCase"
    )


class Court(TableBase, AddressBase, Base):
    __tablename__ = "court"
    name = Column(String(100), unique=True, nullable=False)
    dhs_address = Column(String(1000), nullable=True)
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="court_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(back_populates="courts")
    judges: Mapped[List["Judge"]] = relationship(back_populates="court")
    history_courts: Mapped[List["HistoryCourt"]] = relationship(back_populates="court")
    history_judges: Mapped[List["HistoryJudge"]] = relationship("HistoryJudge")


class HistoryCourt(TableBase, AddressBase, Base):
    __tablename__ = "history_court"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_app_user_id",
        ),
        nullable=False,
    )
    court_id = Column(
        ForeignKey(
            "court.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_court_id",
        ),
        nullable=False,
    )
    name = Column(String(100), nullable=True)
    dhs_address = Column(String(1000), nullable=True)
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_courts"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_courts")
    court: Mapped[Court] = relationship(back_populates="history_courts")


class Judge(TableBase, Base):
    __tablename__ = "judge"
    name = Column(String(100), unique=True, nullable=False)
    webex = Column(String(1000), unique=True, nullable=True)
    court_id = Column(
        ForeignKey(
            "court.id", onupdate="NO ACTION", ondelete="RESTRICT", name="judge_court_id"
        ),
        nullable=False,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="judge_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(back_populates="judges")
    court: Mapped[Court] = relationship(back_populates="judges")
    clients: Mapped[List["Client"]] = relationship(back_populates="judge")
    history_judges: Mapped[List["HistoryJudge"]] = relationship(back_populates="judge")
    history_clients: Mapped[List["HistoryClient"]] = relationship("HistoryClient")


class HistoryJudge(TableBase, Base):
    __tablename__ = "history_judge"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_judge_app_user_id",
        ),
        nullable=False,
    )
    judge_id = Column(
        ForeignKey(
            "judge.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_judge_judge_id",
        ),
        nullable=False,
    )
    name = Column(String(100), nullable=True)
    webex = Column(String(1000), nullable=True)
    court_id = Column(
        ForeignKey(
            "court.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_judge_court_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_judge_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_judges"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_judges")
    judge: Mapped[Judge] = relationship(back_populates="history_judges")
    court: Mapped[Court] = relationship(back_populates="history_judges")


class Client(TableBase, AddressBase, Base):
    __tablename__ = "client"
    name = Column(String(100), unique=True, nullable=False)
    a_number = Column(String(100), unique=True, nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    judge_id = Column(
        ForeignKey(
            "judge.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="client_judge_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="client_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(back_populates="clients")
    judge: Mapped[Judge] = relationship(back_populates="clients")
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="client")
    history_clients: Mapped[List["HistoryClient"]] = relationship(
        back_populates="client"
    )
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        "HistoryCourtCase"
    )


class HistoryClient(TableBase, AddressBase, Base):
    __tablename__ = "history_client"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_client_app_user_id",
        ),
        nullable=False,
    )
    client_id = Column(
        ForeignKey(
            "client.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_client_client_id",
        ),
        nullable=False,
    )
    name = Column(String(100), nullable=True)
    a_number = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    judge_id = Column(
        ForeignKey(
            "judge.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_client_judge_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_client_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_clients"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_clients")
    client: Mapped[Client] = relationship(back_populates="history_clients")
    judge: Mapped[Judge] = relationship(back_populates="history_clients")


class CourtCase(TableBase, Base):
    __tablename__ = "court_case"
    case_type_id = Column(
        ForeignKey(
            "case_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="court_case_case_type_id",
        ),
        nullable=False,
    )
    client_id = Column(
        ForeignKey(
            "client.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="court_case_client_id",
        ),
        nullable=False,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="court_case_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="court_cases"
    )
    case_type: Mapped[CaseType] = relationship(back_populates="court_cases")
    client: Mapped[Client] = relationship(back_populates="court_cases")
    filings: Mapped[List["Filing"]] = relationship(back_populates="court_case")
    case_collections: Mapped[List["CaseCollection"]] = relationship(
        back_populates="court_case"
    )
    hearing_calendars: Mapped[List["HearingCalendar"]] = relationship(
        back_populates="court_case"
    )
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        back_populates="court_case"
    )
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        "HistoryHearingCalendar"
    )
    history_filings: Mapped[List["HistoryFiling"]] = relationship("HistoryFiling")
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        "HistoryCaseCollection"
    )


class HistoryCourtCase(TableBase, Base):
    __tablename__ = "history_court_case"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_case_app_user_id",
        ),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_case_court_case_id",
        ),
        nullable=False,
    )
    case_type_id = Column(
        ForeignKey(
            "case_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_case_case_type_id",
        ),
        nullable=True,
    )
    client_id = Column(
        ForeignKey(
            "client.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_case_client_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_court_case_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_court_cases"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_court_cases")
    court_case: Mapped[CourtCase] = relationship(back_populates="history_court_cases")
    case_type: Mapped[CaseType] = relationship(back_populates="history_court_cases")
    client: Mapped[Client] = relationship(back_populates="history_court_cases")


class HearingCalendar(TableBase, Base):
    __tablename__ = "hearing_calendar"
    hearing_date = Column(DateTime, nullable=False)
    hearing_type_id = Column(
        ForeignKey(
            "hearing_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="hearing_calendar_hearing_type_id",
        ),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="hearing_calendar_court_case_id",
        ),
        nullable=False,
        unique=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="hearing_calendar_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="hearing_calendars"
    )
    hearing_type: Mapped[HearingType] = relationship(back_populates="hearing_calendars")
    court_case: Mapped[CourtCase] = relationship(back_populates="hearing_calendars")
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(
        back_populates="hearing_calendar"
    )
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        back_populates="hearing_calendar"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        "HistoryTaskCalendar"
    )


class HistoryHearingCalendar(TableBase, Base):
    __tablename__ = "history_hearing_calendar"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_hearing_calendar_app_user_id",
        ),
        nullable=False,
    )
    hearing_calendar_id = Column(
        ForeignKey(
            "hearing_calendar.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_hearing_calendar_hearing_calendar_id",
        ),
        nullable=False,
    )
    hearing_date = Column(DateTime, nullable=True)
    hearing_type_id = Column(
        ForeignKey(
            "hearing_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_hearing_calendar_hearing_type_id",
        ),
        nullable=True,
    )
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_hearing_calendar_court_case_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_hearing_calendar_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_hearing_calendars"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_hearing_calendars")
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="history_hearing_calendars"
    )
    hearing_type: Mapped[HearingType] = relationship(
        back_populates="history_hearing_calendars"
    )
    court_case: Mapped[CourtCase] = relationship(
        back_populates="history_hearing_calendars"
    )


class TaskCalendar(TableBase, Base):
    __tablename__ = "task_calendar"
    task_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    task_type_id = Column(
        ForeignKey(
            "task_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="task_calendar_task_type_id",
        ),
        nullable=False,
    )
    hearing_calendar_id = Column(
        ForeignKey(
            "hearing_calendar.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="task_calendar_hearing_calendar_id",
        ),
        nullable=True,
    )
    filing_id = Column(
        ForeignKey(
            "filing.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="task_calendar_filing_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="task_calendar_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="task_calendars"
    )
    task_type: Mapped[TaskType] = relationship(back_populates="task_calendars")
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="task_calendars"
    )
    filing: Mapped["Filing"] = relationship(back_populates="task_calendars")
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        back_populates="task_calendar"
    )


class HistoryTaskCalendar(TableBase, Base):
    __tablename__ = "history_task_calendar"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_task_calendar_app_user_id",
        ),
        nullable=False,
    )
    task_calendar_id = Column(
        ForeignKey(
            "task_calendar.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_task_calendar_task_calendar_id",
        ),
        nullable=False,
    )
    task_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    task_type_id = Column(
        ForeignKey(
            "task_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_task_calendar_task_type_id",
        ),
        nullable=True,
    )
    hearing_calendar_id = Column(
        ForeignKey(
            "hearing_calendar.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_task_calendar_hearing_calendar_id",
        ),
        nullable=True,
    )
    filing_id = Column(
        ForeignKey(
            "filing.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_task_calendar_filing_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_task_calendar_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_task_calendars"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_task_calendars")
    task_calendar: Mapped[TaskCalendar] = relationship(
        back_populates="history_task_calendars"
    )
    task_type: Mapped[TaskType] = relationship(back_populates="history_task_calendars")
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="history_task_calendars"
    )
    filing: Mapped["Filing"] = relationship(back_populates="history_task_calendars")


class Filing(TableBase, Base):
    __tablename__ = "filing"
    submit_date = Column(DateTime, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    receipt_number = Column(String(100), nullable=True)
    priority_date = Column(DateTime, nullable=True)
    rfe_date = Column(DateTime, nullable=True)
    rfe_submit_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    filing_type_id = Column(
        ForeignKey(
            "filing_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="filing_filing_type_id",
        ),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="filing_court_case_id",
        ),
        nullable=False,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="filing_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(back_populates="filings")
    filing_type: Mapped[FilingType] = relationship(back_populates="filings")
    court_case: Mapped[CourtCase] = relationship(back_populates="filings")
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(back_populates="filing")
    history_filings: Mapped[List["HistoryFiling"]] = relationship(
        back_populates="filing"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        "HistoryTaskCalendar"
    )


class HistoryFiling(TableBase, Base):
    __tablename__ = "history_filing"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_filing_app_user_id",
        ),
        nullable=False,
    )
    filing_id = Column(
        ForeignKey(
            "filing.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_filing_filing_id",
        ),
        nullable=False,
    )
    submit_date = Column(DateTime, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    receipt_number = Column(String(100), nullable=True)
    priority_date = Column(DateTime, nullable=True)
    rfe_date = Column(DateTime, nullable=True)
    rfe_submit_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    filing_type_id = Column(
        ForeignKey(
            "filing_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_filing_filing_type_id",
        ),
        nullable=True,
    )
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_filing_court_case_id",
        ),
        nullable=True,
    )
    task_calendar_id = Column(
        ForeignKey(
            "task_calendar.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_filing_task_calendar_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_filing_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_filings"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_filings")
    filing: Mapped[Filing] = relationship(back_populates="history_filings")
    filing_type: Mapped[FilingType] = relationship(back_populates="history_filings")
    court_case: Mapped[CourtCase] = relationship(back_populates="history_filings")


class CaseCollection(TableBase, Base):
    __tablename__ = "case_collection"
    quote_amount = Column(Numeric(precision=7, scale=2), nullable=False)
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="case_collection_court_case_id",
        ),
        nullable=False,
        unique=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="case_collection_component_status_id",
        ),
        nullable=False,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="case_collections"
    )
    court_case: Mapped[CourtCase] = relationship(back_populates="case_collections")
    cash_collections: Mapped[List["CashCollection"]] = relationship(
        back_populates="case_collection"
    )
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        back_populates="case_collection"
    )
    history_cash_collections: Mapped[List["HistoryCashCollection"]] = relationship(
        "HistoryCashCollection"
    )


class HistoryCaseCollection(TableBase, Base):
    __tablename__ = "history_case_collection"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_case_collection_app_user_id",
        ),
        nullable=False,
    )
    case_collection_id = Column(
        ForeignKey(
            "case_collection.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_case_collection_case_collection_id",
        ),
        nullable=False,
    )
    quote_amount = Column(Numeric(precision=7, scale=2), nullable=True)
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_case_collection_court_case_id",
        ),
        nullable=True,
    )
    component_status_id = Column(
        ForeignKey(
            "component_status.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_case_collection_component_status_id",
        ),
        nullable=True,
    )
    comments = Column(String(10000), nullable=True)
    component_status: Mapped[ComponentStatus] = relationship(
        back_populates="history_case_collections"
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_case_collections")
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="history_case_collections"
    )
    court_case: Mapped[CourtCase] = relationship(
        back_populates="history_case_collections"
    )


class CashCollection(TableBase, Base):
    __tablename__ = "cash_collection"
    collection_date = Column(DateTime, nullable=False)
    collected_amount = Column(Numeric(precision=7, scale=2), nullable=False)
    waived_amount = Column(Numeric(precision=7, scale=2), nullable=False)
    memo = Column(String(3000), nullable=False)
    case_collection_id = Column(
        ForeignKey(
            "case_collection.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="cash_collection_case_collection_id",
        ),
        nullable=False,
    )
    collection_method_id = Column(
        ForeignKey(
            "collection_method.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="cash_collection_collection_method_id",
        ),
        nullable=False,
    )
    collection_method: Mapped[CollectionMethod] = relationship(
        back_populates="cash_collections"
    )
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="cash_collections"
    )
    history_cash_collections: Mapped[List["HistoryCashCollection"]] = relationship(
        back_populates="cash_collection"
    )


class HistoryCashCollection(TableBase, Base):
    __tablename__ = "history_cash_collection"
    app_user_id = Column(
        ForeignKey(
            "app_user.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_cash_collection_app_user_id",
        ),
        nullable=False,
    )
    cash_collection_id = Column(
        ForeignKey(
            "cash_collection.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_cash_collection_cash_collection_id",
        ),
        nullable=False,
    )
    collection_date = Column(DateTime, nullable=True)
    collected_amount = Column(Numeric(precision=7, scale=2), nullable=True)
    waived_amount = Column(Numeric(precision=7, scale=2), nullable=True)
    memo = Column(String(3000), nullable=True)
    case_collection_id = Column(
        ForeignKey(
            "case_collection.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_cash_collection_case_collection_id",
        ),
        nullable=True,
    )
    collection_method_id = Column(
        ForeignKey(
            "collection_method.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_cash_collection_collection_method_id",
        ),
        nullable=True,
    )
    app_user: Mapped[AppUser] = relationship(back_populates="history_cash_collections")
    cash_collection: Mapped[CashCollection] = relationship(
        back_populates="history_cash_collections"
    )
    collection_method: Mapped[CollectionMethod] = relationship(
        back_populates="history_cash_collections"
    )
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="history_cash_collections"
    )
