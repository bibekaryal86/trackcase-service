from typing import Any, List

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

Base: Any = declarative_base()


class TableBase:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)


class NameDescBase:
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(3000), nullable=False)


class StatusBase:
    status = Column(String(100), nullable=False)
    comments = Column(String(10000), unique=False, nullable=True)


class AddressBase:
    street_address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(10), nullable=True)
    zip_code = Column(String(10), nullable=True)
    phone_number = Column(String(25), nullable=True)


class FormType(TableBase, NameDescBase, Base):
    __tablename__ = "form_type"
    forms: Mapped[List["Form"]] = relationship(back_populates="form_type")
    history_forms: Mapped[List["HistoryForm"]] = relationship("HistoryForm")


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


class Court(TableBase, AddressBase, StatusBase, Base):
    __tablename__ = "court"
    name = Column(String(100), unique=True, nullable=False)
    dhs_address = Column(String(1000), nullable=True)
    judges: Mapped[List["Judge"]] = relationship(back_populates="court")
    history_courts: Mapped[List["HistoryCourt"]] = relationship(back_populates="court")
    history_judges: Mapped[List["HistoryJudge"]] = relationship("HistoryJudge")


class HistoryCourt(TableBase, AddressBase, StatusBase, Base):
    __tablename__ = "history_court"
    user_name = Column(String(100), nullable=False)
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
    court: Mapped[Court] = relationship(back_populates="history_courts")


class Judge(TableBase, StatusBase, Base):
    __tablename__ = "judge"
    name = Column(String(100), unique=True, nullable=False)
    webex = Column(String(1000), unique=True, nullable=True)
    court_id = Column(
        ForeignKey(
            "court.id", onupdate="NO ACTION", ondelete="RESTRICT", name="judge_court_id"
        ),
        nullable=False,
    )
    court: Mapped[Court] = relationship(back_populates="judges")
    clients: Mapped[List["Client"]] = relationship(back_populates="judge")
    history_judges: Mapped[List["HistoryJudge"]] = relationship(back_populates="judge")
    history_clients: Mapped[List["HistoryClient"]] = relationship("HistoryClient")


class HistoryJudge(TableBase, StatusBase, Base):
    __tablename__ = "history_judge"
    user_name = Column(String(100), nullable=False)
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
    judge: Mapped[Judge] = relationship(back_populates="history_judges")
    court: Mapped[Court] = relationship(back_populates="history_judges")


class Client(TableBase, AddressBase, StatusBase, Base):
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
    judge: Mapped[Judge] = relationship(back_populates="clients")
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="client")
    history_clients: Mapped[List["HistoryClient"]] = relationship(
        back_populates="client"
    )
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        "HistoryCourtCase"
    )


class HistoryClient(TableBase, AddressBase, StatusBase, Base):
    __tablename__ = "history_client"
    user_name = Column(String(100), nullable=False)
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
    client: Mapped[Client] = relationship(back_populates="history_clients")
    judge: Mapped[Judge] = relationship(back_populates="history_clients")


class CourtCase(TableBase, StatusBase, Base):
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
    case_type: Mapped[CaseType] = relationship(back_populates="court_cases")
    client: Mapped[Client] = relationship(back_populates="court_cases")
    forms: Mapped[List["Form"]] = relationship(back_populates="court_case")
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
    history_forms: Mapped[List["HistoryForm"]] = relationship("HistoryForm")
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        "HistoryCaseCollection"
    )


class HistoryCourtCase(TableBase, StatusBase, Base):
    __tablename__ = "history_court_case"
    user_name = Column(String(100), nullable=False)
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
    court_case: Mapped[CourtCase] = relationship(back_populates="history_court_cases")
    case_type: Mapped[CaseType] = relationship(back_populates="history_court_cases")
    client: Mapped[Client] = relationship(back_populates="history_court_cases")


class HearingCalendar(TableBase, StatusBase, Base):
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


class HistoryHearingCalendar(TableBase, StatusBase, Base):
    __tablename__ = "history_hearing_calendar"
    user_name = Column(String(100), nullable=False)
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
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="history_hearing_calendars"
    )
    hearing_type: Mapped[HearingType] = relationship(
        back_populates="history_hearing_calendars"
    )
    court_case: Mapped[CourtCase] = relationship(
        back_populates="history_hearing_calendars"
    )


class TaskCalendar(TableBase, StatusBase, Base):
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
    form_id = Column(
        ForeignKey(
            "form.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="task_calendar_form_id",
        ),
        nullable=True,
    )
    task_type: Mapped[TaskType] = relationship(back_populates="task_calendars")
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="task_calendars"
    )
    form: Mapped["Form"] = relationship(back_populates="task_calendars")
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        back_populates="task_calendar"
    )


class HistoryTaskCalendar(TableBase, StatusBase, Base):
    __tablename__ = "history_task_calendar"
    user_name = Column(String(100), nullable=False)
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
    form_id = Column(
        ForeignKey(
            "form.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_task_calendar_form_id",
        ),
        nullable=True,
    )
    task_calendar: Mapped[TaskCalendar] = relationship(
        back_populates="history_task_calendars"
    )
    task_type: Mapped[TaskType] = relationship(back_populates="history_task_calendars")
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="history_task_calendars"
    )
    form: Mapped["Form"] = relationship(back_populates="history_task_calendars")


class Form(TableBase, StatusBase, Base):
    __tablename__ = "form"
    submit_date = Column(DateTime, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    receipt_number = Column(String(100), nullable=True)
    priority_date = Column(DateTime, nullable=True)
    rfe_date = Column(DateTime, nullable=True)
    rfe_submit_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    form_type_id = Column(
        ForeignKey(
            "form_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="form_form_type_id",
        ),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="form_court_case_id",
        ),
        nullable=False,
    )
    form_type: Mapped[FormType] = relationship(back_populates="forms")
    court_case: Mapped[CourtCase] = relationship(back_populates="forms")
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(back_populates="form")
    history_forms: Mapped[List["HistoryForm"]] = relationship(back_populates="form")
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        "HistoryTaskCalendar"
    )


class HistoryForm(TableBase, StatusBase, Base):
    __tablename__ = "history_form"
    user_name = Column(String(100), nullable=False)
    form_id = Column(
        ForeignKey(
            "form.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_form_form_id",
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
    form_type_id = Column(
        ForeignKey(
            "form_type.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_form_form_type_id",
        ),
        nullable=True,
    )
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_form_court_case_id",
        ),
        nullable=True,
    )
    task_calendar_id = Column(
        ForeignKey(
            "task_calendar.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_form_task_calendar_id",
        ),
        nullable=True,
    )
    form: Mapped[Form] = relationship(back_populates="history_forms")
    form_type: Mapped[FormType] = relationship(back_populates="history_forms")
    court_case: Mapped[CourtCase] = relationship(back_populates="history_forms")


class CaseCollection(TableBase, StatusBase, Base):
    __tablename__ = "case_collection"
    quote_date = Column(DateTime, nullable=False)
    quote_amount = Column(BigInteger, nullable=False)
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


class HistoryCaseCollection(TableBase, StatusBase, Base):
    __tablename__ = "history_case_collection"
    user_name = Column(String(100), nullable=False)
    case_collection_id = Column(
        ForeignKey(
            "case_collection.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_case_collection_case_collection_id",
        ),
        nullable=False,
    )
    quote_date = Column(DateTime, nullable=True)
    quote_amount = Column(BigInteger, nullable=True)
    court_case_id = Column(
        ForeignKey(
            "court_case.id",
            onupdate="NO ACTION",
            ondelete="RESTRICT",
            name="history_case_collection_court_case_id",
        ),
        nullable=True,
    )
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="history_case_collections"
    )
    court_case: Mapped[CourtCase] = relationship(
        back_populates="history_case_collections"
    )


class CashCollection(TableBase, StatusBase, Base):
    __tablename__ = "cash_collection"
    collection_date = Column(DateTime, nullable=False)
    collected_amount = Column(BigInteger, nullable=False)
    waived_amount = Column(BigInteger, nullable=False)
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


class HistoryCashCollection(TableBase, StatusBase, Base):
    __tablename__ = "history_cash_collection"
    user_name = Column(String(100), nullable=False)
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
    collected_amount = Column(BigInteger, nullable=True)
    waived_amount = Column(BigInteger, nullable=True)
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
    cash_collection: Mapped[CashCollection] = relationship(
        back_populates="history_cash_collections"
    )
    collection_method: Mapped[CollectionMethod] = relationship(
        back_populates="history_cash_collections"
    )
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="history_cash_collections"
    )
