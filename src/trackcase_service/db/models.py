from typing import Any, List

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

Base: Any = declarative_base()


class TableBase:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, server_default=func.sysdate(), nullable=False)
    modified = Column(DateTime, server_default=func.sysdate(), nullable=False)


class FormType(TableBase, Base):
    __tablename__ = "form_type"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)
    forms: Mapped[List["Form"]] = relationship(back_populates="form_type")
    history_forms: Mapped[List["HistoryForm"]] = relationship(
        back_populates="form_type"
    )


class FormStatus(TableBase, Base):
    __tablename__ = "form_status"
    name: str = Column(String(25), unique=True, nullable=False)
    description: str = Column(String(280), nullable=False)
    forms: Mapped[List["Form"]] = relationship(back_populates="form_status")
    history_forms: Mapped[List["HistoryForm"]] = relationship(
        back_populates="form_status"
    )


class CollectionMethod(TableBase, Base):
    __tablename__ = "collection_method"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)
    case_collections: Mapped[List["CaseCollection"]] = relationship(
        back_populates="collection_method"
    )
    cash_collections: Mapped[List["CashCollection"]] = relationship(
        back_populates="collection_method"
    )


class HearingType(TableBase, Base):
    __tablename__ = "hearing_type"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)
    hearing_calendars: Mapped[List["HearingCalendar"]] = relationship(
        back_populates="hearing_type"
    )


class TaskType(TableBase, Base):
    __tablename__ = "task_type"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(
        back_populates="task_type"
    )


class CaseType(TableBase, Base):
    __tablename__ = "case_type"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="case_type")


class Court(TableBase, Base):
    __tablename__ = "court"
    name = Column(String(25), unique=True, nullable=False)
    address = Column(String(100), unique=True, nullable=False)
    dhs_address = Column(String(100), unique=True, nullable=True)
    judges: Mapped[List["Judge"]] = relationship(back_populates="court")


class Judge(TableBase, Base):
    __tablename__ = "judge"
    name = Column(String(25), unique=True, nullable=False)
    webex = Column(String(100), unique=True, nullable=True)
    court_id = Column(
        ForeignKey("court.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    court: Mapped[Court] = relationship(back_populates="judges")
    clients: Mapped[List["Client"]] = relationship(back_populates="judge")


class Client(TableBase, Base):
    __tablename__ = "client"
    name = Column(String(50), unique=True, nullable=False)
    a_number = Column(String(10), unique=True, nullable=True)
    address = Column(String(100), nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    email = Column(DateTime, unique=True, nullable=True)
    judge_id = Column(
        ForeignKey("judge.id", onupdate="NO ACTION", ondelete="RESTRICT"), nullable=True
    )
    judge: Mapped[Judge] = relationship(back_populates="clients")
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="client")


class CourtCase(TableBase, Base):
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
    history_forms: Mapped[List["HistoryForm"]] = relationship(
        back_populates="court_case"
    )


class HearingCalendar(TableBase, Base):
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


class TaskCalendar(TableBase, Base):
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
    forms: Mapped["Form"] = relationship(back_populates="task_calendar")
    history_forms: Mapped[List["HistoryForm"]] = relationship(
        back_populates="form_type"
    )


class Form(TableBase, Base):
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
    form_status_id = Column(
        ForeignKey("form_status.id", onupdate="NO ACTION", ondelete="RESTRICT"),
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
    form_status: Mapped[FormStatus] = relationship(back_populates="forms")
    form_type: Mapped[FormType] = relationship(back_populates="forms")
    task_calendar: Mapped[TaskCalendar] = relationship(back_populates="forms")
    court_case: Mapped[CourtCase] = relationship(back_populates="forms")
    case_collections: Mapped[List["CaseCollection"]] = relationship(
        back_populates="form"
    )
    history_forms: Mapped[List["HistoryForm"]] = relationship(back_populates="form")


class CaseCollection(TableBase, Base):
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
    court_case: Mapped[CourtCase] = relationship(
        back_populates="case_collections"
    )
    form: Mapped[Form] = relationship(back_populates="case_collections")
    cash_collections: Mapped[List["CashCollection"]] = relationship(back_populates="case_collection")


class CashCollection(TableBase, Base):
    __tablename__ = "cash_collection"
    collection_date = Column(DateTime, nullable=False)
    collected_amount = Column(BigInteger, nullable=False)
    waived_amount = Column(BigInteger, nullable=False)
    memo = Column(String(280), nullable=True)
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


class HistoryForm(TableBase, Base):
    __tablename__ = "history_form"
    user_name = Column(String(25), nullable=False)
    submit_date = Column(DateTime, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    rfe_date = Column(DateTime, nullable=True)
    rfe_submit_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    form_id = Column(
        ForeignKey("form.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    form_type_id = Column(
        ForeignKey("form_type.id", onupdate="NO ACTION", ondelete="RESTRICT"),
        nullable=False,
    )
    form_status_id = Column(
        ForeignKey("form_status.id", onupdate="NO ACTION", ondelete="RESTRICT"),
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
    form: Mapped[Form] = relationship(back_populates="history_forms")
    form_status: Mapped[FormStatus] = relationship(back_populates="history_forms")
    form_type: Mapped[FormType] = relationship(back_populates="history_forms")
    task_calendar: Mapped[TaskCalendar] = relationship(back_populates="history_forms")
    court_case: Mapped[CourtCase] = relationship(back_populates="history_forms")
