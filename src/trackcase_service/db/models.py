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


class NoteBase:
    user_name = Column(String(100), nullable=False)
    note = Column(String(3000), nullable=False)


class FormType(TableBase, NameDescBase, Base):
    __tablename__ = "form_type"
    forms: Mapped[List["Form"]] = relationship(back_populates="form_type")
    history_forms: Mapped[List["HistoryForm"]] = relationship(
        back_populates="form_type"
    )


class CollectionMethod(TableBase, NameDescBase, Base):
    __tablename__ = "collection_method"
    case_collections: Mapped[List["CaseCollection"]] = relationship(
        back_populates="collection_method"
    )
    cash_collections: Mapped[List["CashCollection"]] = relationship(
        back_populates="collection_method"
    )
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        back_populates="collection_method"
    )
    history_cash_collections: Mapped[List["HistoryCashCollection"]] = relationship(
        back_populates="collection_method"
    )


class HearingType(TableBase, NameDescBase, Base):
    __tablename__ = "hearing_type"
    hearing_calendars: Mapped[List["HearingCalendar"]] = relationship(
        back_populates="hearing_type"
    )
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        back_populates="hearing_type"
    )


class TaskType(TableBase, NameDescBase, Base):
    __tablename__ = "task_type"
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(
        back_populates="task_type"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        back_populates="task_type"
    )


class CaseType(TableBase, NameDescBase, Base):
    __tablename__ = "case_type"
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="case_type")
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        back_populates="case_type"
    )


class Court(TableBase, AddressBase, StatusBase, Base):
    __tablename__ = "court"
    name = Column(String(100), unique=True, nullable=False)
    dhs_address = Column(String(1000), nullable=True)
    judges: Mapped[List["Judge"]] = relationship(back_populates="court")
    note_courts: Mapped[List["NoteCourt"]] = relationship(back_populates="court")
    history_courts: Mapped[List["HistoryCourt"]] = relationship(back_populates="court")
    history_judges: Mapped[List["HistoryJudge"]] = relationship(back_populates="court")


class NoteCourt(TableBase, NoteBase, Base):
    __tablename__ = "note_court"
    court_id = Column(
        ForeignKey("court.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court: Mapped[Court] = relationship(back_populates="note_courts")


class HistoryCourt(TableBase, AddressBase, StatusBase, Base):
    __tablename__ = "history_court"
    user_name = Column(String(100), nullable=False)
    court_id = Column(
        ForeignKey("court.id", onupdate="NO ACTION", ondelete="RESTRICT"),
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
        ForeignKey("court.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court: Mapped[Court] = relationship(back_populates="judges")
    clients: Mapped[List["Client"]] = relationship(back_populates="judge")
    note_judges: Mapped[List["NoteJudge"]] = relationship(back_populates="judge")
    history_judges: Mapped[List["HistoryJudge"]] = relationship(back_populates="judge")
    history_clients: Mapped[List["HistoryClient"]] = relationship(
        back_populates="judge"
    )


class NoteJudge(TableBase, NoteBase, Base):
    __tablename__ = "note_judge"
    judge_id = Column(
        ForeignKey("judge.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    judge: Mapped[Judge] = relationship(back_populates="note_judges")


class HistoryJudge(TableBase, StatusBase, Base):
    __tablename__ = "history_judge"
    user_name = Column(String(100), nullable=False)
    judge_id = Column(
        ForeignKey("judge.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    name = Column(String(100), nullable=True)
    webex = Column(String(1000), nullable=True)
    court_id = Column(
        ForeignKey("court.id", onupdate="NO ACTION", ondelete="RESTRICT"),
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
        ForeignKey("judge.id", onupdate="NO ACTION", ondelete="RESTRICT"), nullable=True
    )
    judge: Mapped[Judge] = relationship(back_populates="clients")
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="client")
    note_clients: Mapped[List["NoteClient"]] = relationship(back_populates="client")
    history_clients: Mapped[List["HistoryClient"]] = relationship(
        back_populates="client"
    )
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        back_populates="client"
    )


class NoteClient(TableBase, NoteBase, Base):
    __tablename__ = "note_client"
    client_id = Column(
        ForeignKey("client.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    client: Mapped[Client] = relationship(back_populates="note_clients")


class HistoryClient(TableBase, AddressBase, StatusBase, Base):
    __tablename__ = "history_client"
    user_name = Column(String(100), nullable=False)
    client_id = Column(
        ForeignKey("client.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    name = Column(String(100), nullable=True)
    a_number = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    judge_id = Column(
        ForeignKey("judge.id", onupdate="NO ACTION", ondelete="RESTRICT"), nullable=True
    )
    client: Mapped[Client] = relationship(back_populates="history_clients")
    judge: Mapped[Judge] = relationship(back_populates="history_clients")


class CourtCase(TableBase, StatusBase, Base):
    __tablename__ = "court_case"
    case_type_id = Column(
        ForeignKey("case_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    client_id = Column(
        ForeignKey("client.id", onupdate="NO ACTION", ondelete="RESTRICT"),
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
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(
        back_populates="court_case"
    )
    note_court_cases: Mapped[List["NoteCourtCase"]] = relationship(
        back_populates="court_case"
    )
    history_court_cases: Mapped[List["HistoryCourtCase"]] = relationship(
        back_populates="court_case"
    )
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        back_populates="court_case"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        back_populates="court_case"
    )
    history_forms: Mapped[List["HistoryForm"]] = relationship(
        back_populates="court_case"
    )
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        back_populates="court_case"
    )


class NoteCourtCase(TableBase, NoteBase, Base):
    __tablename__ = "note_court_case"
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case: Mapped[CourtCase] = relationship(back_populates="note_court_cases")


class HistoryCourtCase(TableBase, StatusBase, Base):
    __tablename__ = "history_court_case"
    user_name = Column(String(100), nullable=False)
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    case_type_id = Column(
        ForeignKey("case_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    client_id = Column(
        ForeignKey("client.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    court_case: Mapped[CourtCase] = relationship(back_populates="history_court_cases")
    case_type: Mapped[CaseType] = relationship(back_populates="history_court_cases")
    client: Mapped[Client] = relationship(back_populates="history_court_cases")


class HearingCalendar(TableBase, StatusBase, Base):
    __tablename__ = "hearing_calendar"
    hearing_date = Column(DateTime, nullable=False)
    hearing_type_id = Column(
        ForeignKey("hearing_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    hearing_type: Mapped[HearingType] = relationship(back_populates="hearing_calendars")
    court_case: Mapped[CourtCase] = relationship(back_populates="hearing_calendars")
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(
        back_populates="hearing_calendar"
    )
    note_hearing_calendars: Mapped[List["NoteHearingCalendar"]] = relationship(
        back_populates="hearing_calendar"
    )
    history_hearing_calendars: Mapped[List["HistoryHearingCalendar"]] = relationship(
        back_populates="hearing_calendar"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        back_populates="hearing_calendar"
    )


class NoteHearingCalendar(TableBase, NoteBase, Base):
    __tablename__ = "note_hearing_calendar"
    hearing_calendar_id = Column(
        ForeignKey("hearing_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="note_hearing_calendars"
    )


class HistoryHearingCalendar(TableBase, StatusBase, Base):
    __tablename__ = "history_hearing_calendar"
    user_name = Column(String(100), nullable=False)
    hearing_calendar_id = Column(
        ForeignKey("hearing_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    hearing_date = Column(DateTime, nullable=True)
    hearing_type_id = Column(
        ForeignKey("hearing_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
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
    task_type_id = Column(
        ForeignKey("task_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    hearing_calendar_id = Column(
        ForeignKey("hearing_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    task_type: Mapped[TaskType] = relationship(back_populates="task_calendars")
    court_case: Mapped[CourtCase] = relationship(back_populates="task_calendars")
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="task_calendars"
    )
    forms: Mapped[List["Form"]] = relationship(back_populates="task_calendar")
    note_task_calendars: Mapped[List["NoteTaskCalendar"]] = relationship(
        back_populates="task_calendar"
    )
    history_task_calendars: Mapped[List["HistoryTaskCalendar"]] = relationship(
        back_populates="task_calendar"
    )
    history_forms: Mapped[List["HistoryForm"]] = relationship(
        back_populates="task_calendar"
    )


class NoteTaskCalendar(TableBase, NoteBase, Base):
    __tablename__ = "note_task_calendar"
    task_calendar_id = Column(
        ForeignKey("task_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    task_calendar: Mapped[TaskCalendar] = relationship(
        back_populates="note_task_calendars"
    )


class HistoryTaskCalendar(TableBase, StatusBase, Base):
    __tablename__ = "history_task_calendar"
    user_name = Column(String(100), nullable=False)
    task_calendar_id = Column(
        ForeignKey("task_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    task_date = Column(DateTime, nullable=True)
    task_type_id = Column(
        ForeignKey("task_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    hearing_calendar_id = Column(
        ForeignKey("hearing_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    task_calendar: Mapped[TaskCalendar] = relationship(
        back_populates="history_task_calendars"
    )
    task_type: Mapped[TaskType] = relationship(back_populates="history_task_calendars")
    court_case: Mapped[CourtCase] = relationship(
        back_populates="history_task_calendars"
    )
    hearing_calendar: Mapped[HearingCalendar] = relationship(
        back_populates="history_task_calendars"
    )


class Form(TableBase, StatusBase, Base):
    __tablename__ = "form"
    submit_date = Column(DateTime, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    rfe_date = Column(DateTime, nullable=True)
    rfe_submit_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    form_type_id = Column(
        ForeignKey("form_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    task_calendar_id = Column(
        ForeignKey("task_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    form_type: Mapped[FormType] = relationship(back_populates="forms")
    task_calendar: Mapped[TaskCalendar] = relationship(back_populates="forms")
    court_case: Mapped[CourtCase] = relationship(back_populates="forms")
    case_collections: Mapped[List["CaseCollection"]] = relationship(
        back_populates="form"
    )
    note_forms: Mapped[List["NoteForm"]] = relationship(back_populates="form")
    history_forms: Mapped[List["HistoryForm"]] = relationship(back_populates="form")
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        back_populates="form"
    )


class NoteForm(TableBase, NoteBase, Base):
    __tablename__ = "note_form"
    form_id = Column(
        ForeignKey("form.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    form: Mapped[Form] = relationship(back_populates="note_forms")


class HistoryForm(TableBase, StatusBase, Base):
    __tablename__ = "history_form"
    user_name = Column(String(100), nullable=False)
    form_id = Column(
        ForeignKey("form.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    submit_date = Column(DateTime, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    rfe_date = Column(DateTime, nullable=True)
    rfe_submit_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    form_type_id = Column(
        ForeignKey("form_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    task_calendar_id = Column(
        ForeignKey("task_calendar.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    form: Mapped[Form] = relationship(back_populates="history_forms")
    form_type: Mapped[FormType] = relationship(back_populates="history_forms")
    task_calendar: Mapped[TaskCalendar] = relationship(back_populates="history_forms")
    court_case: Mapped[CourtCase] = relationship(back_populates="history_forms")


class CaseCollection(TableBase, StatusBase, Base):
    __tablename__ = "case_collection"
    quote_date = Column(DateTime, nullable=False)
    quote_amount = Column(BigInteger, nullable=False)
    initial_payment = Column(BigInteger, nullable=False)
    collection_method_id = Column(
        ForeignKey("collection_method.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    form_id = Column(
        ForeignKey("form.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    collection_method: Mapped[CollectionMethod] = relationship(
        back_populates="case_collections"
    )
    court_case: Mapped[CourtCase] = relationship(back_populates="case_collections")
    form: Mapped[Form] = relationship(back_populates="case_collections")
    cash_collections: Mapped[List["CashCollection"]] = relationship(
        back_populates="case_collection"
    )
    note_case_collections: Mapped[List["NoteCaseCollection"]] = relationship(
        back_populates="case_collection"
    )
    history_case_collections: Mapped[List["HistoryCaseCollection"]] = relationship(
        back_populates="case_collection"
    )
    history_cash_collections: Mapped[List["HistoryCashCollection"]] = relationship(
        back_populates="case_collection"
    )


class NoteCaseCollection(TableBase, NoteBase, Base):
    __tablename__ = "note_case_collection"
    case_collection_id = Column(
        ForeignKey("case_collection.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="note_case_collections"
    )


class HistoryCaseCollection(TableBase, StatusBase, Base):
    __tablename__ = "history_case_collection"
    user_name = Column(String(100), nullable=False)
    case_collection_id = Column(
        ForeignKey("case_collection.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    quote_date = Column(DateTime, nullable=True)
    quote_amount = Column(BigInteger, nullable=True)
    initial_payment = Column(BigInteger, nullable=True)
    collection_method_id = Column(
        ForeignKey("collection_method.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    court_case_id = Column(
        ForeignKey("court_case.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    form_id = Column(
        ForeignKey("form.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="history_case_collections"
    )
    collection_method: Mapped[CollectionMethod] = relationship(
        back_populates="history_case_collections"
    )
    court_case: Mapped[CourtCase] = relationship(
        back_populates="history_case_collections"
    )
    form: Mapped[Form] = relationship(back_populates="history_case_collections")


class CashCollection(TableBase, StatusBase, Base):
    __tablename__ = "cash_collection"
    collection_date = Column(DateTime, nullable=False)
    collected_amount = Column(BigInteger, nullable=False)
    waived_amount = Column(BigInteger, nullable=False)
    memo = Column(String(3000), nullable=True)
    case_collection_id = Column(
        ForeignKey("case_collection.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    collection_method_id = Column(
        ForeignKey("collection_method.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    collection_method: Mapped[CollectionMethod] = relationship(
        back_populates="cash_collections"
    )
    case_collection: Mapped[CaseCollection] = relationship(
        back_populates="cash_collections"
    )
    note_cash_collections: Mapped[List["NoteCashCollection"]] = relationship(
        back_populates="cash_collection"
    )
    history_cash_collections: Mapped[List["HistoryCashCollection"]] = relationship(
        back_populates="cash_collection"
    )


class NoteCashCollection(TableBase, NoteBase, Base):
    __tablename__ = "note_cash_collection"
    cash_collection_id = Column(
        ForeignKey("cash_collection.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    cash_collection: Mapped[CashCollection] = relationship(
        back_populates="note_cash_collections"
    )


class HistoryCashCollection(TableBase, StatusBase, Base):
    __tablename__ = "history_cash_collection"
    user_name = Column(String(100), nullable=False)
    cash_collection_id = Column(
        ForeignKey("cash_collection.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    collection_date = Column(DateTime, nullable=True)
    collected_amount = Column(BigInteger, nullable=True)
    waived_amount = Column(BigInteger, nullable=True)
    memo = Column(String(3000), nullable=True)
    case_collection_id = Column(
        ForeignKey("case_collection.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=True,
    )
    collection_method_id = Column(
        ForeignKey("collection_method.id", onupdate="NO ACTION", ondelete="RESTRICT"),
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


class ZestTable(Base):
    __tablename__ = "zest_table"
    test = Column(String(100), primary_key=True, nullable=False)
