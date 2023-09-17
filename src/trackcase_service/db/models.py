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


class FormStatus(TableBase, Base):
    __tablename__ = "form_status"
    name: str = Column(String(25), unique=True, nullable=False)
    description: str = Column(String(280), nullable=False)
    forms: Mapped[List["Form"]] = relationship(back_populates="form_status")


class CollectionMethod(TableBase, Base):
    __tablename__ = "collection_method"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)
    collections: Mapped[List["Collection"]] = relationship(
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
        ForeignKey("court.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    court: Mapped[Court] = relationship(back_populates="judges")
    clients: Mapped[List["Client"]] = relationship(back_populates="judge")


class Form(TableBase, Base):
    __tablename__ = "form"
    submit_date = Column(DateTime, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    rfe_date = Column(DateTime, nullable=True)
    rfe_submit_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    form_status_id = Column(
        ForeignKey("form_status.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    form_type_id = Column(
        ForeignKey("form_type.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    form_status: Mapped["FormStatus"] = relationship(back_populates="forms")
    form_type: Mapped["FormType"] = relationship(back_populates="forms")
    task_calendar_forms: Mapped[List["TaskCalendarForm"]] = relationship(
        back_populates="form"
    )
    court_case_forms: Mapped[List["CourtCaseForm"]] = relationship(
        back_populates="form"
    )


class Client(TableBase, Base):
    __tablename__ = "client"
    name = Column(String(50), unique=True, nullable=False)
    a_number = Column(String(10), unique=True, nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    email = Column(DateTime, unique=True, nullable=True)
    judge_id = Column(
        ForeignKey("judge.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    judge: Mapped["Judge"] = relationship(back_populates="clients")
    task_calendar_forms: Mapped[List["TaskCalendarForm"]] = relationship(
        back_populates="task_calendar"
    )
    court_cases: Mapped[List["CourtCase"]] = relationship(back_populates="client")


class Collection(TableBase, Base):
    __tablename__ = "collection"
    collection_date = Column(DateTime, nullable=False)
    quote_amount = Column(BigInteger, nullable=False)
    collected_amount = Column(BigInteger, nullable=True)
    collection_method_id = Column(
        ForeignKey("collection_method.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    collection_method: Mapped["CollectionMethod"] = relationship(
        back_populates="collections"
    )
    court_case_collections: Mapped[List["CourtCaseCollection"]] = relationship(
        back_populates="collection"
    )


class HearingCalendar(TableBase, Base):
    __tablename__ = "hearing_calendar"
    hearing_date = Column(DateTime, nullable=False)
    hearing_type_id = Column(
        ForeignKey("hearing_type.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    hearing_type: Mapped["HearingType"] = relationship(
        back_populates="hearing_calendars"
    )
    task_calendars: Mapped[List["TaskCalendar"]] = relationship(
        back_populates="hearing_calendar"
    )
    court_case_hearing_calendars: Mapped[
        List["CourtCaseHearingCalendar"]
    ] = relationship(back_populates="hearing_calendar")


class TaskCalendar(TableBase, Base):
    __tablename__ = "task_calendar"
    task_date = Column(DateTime, nullable=False)
    task_type_id = Column(
        ForeignKey("task_type.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    hearing_calendar_id = Column(
        ForeignKey("hearing_calendar.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    task_type: Mapped["TaskType"] = relationship(back_populates="task_calendars")
    hearing_calendar: Mapped["HearingCalendar"] = relationship(
        back_populates="task_calendars"
    )
    task_calendar_forms: Mapped[List["TaskCalendarForm"]] = relationship(
        back_populates="task_calendar"
    )
    court_case_task_calendars: Mapped[List["CourtCaseTaskCalendar"]] = relationship(
        back_populates="task_calendar"
    )


class TaskCalendarForm(TableBase, Base):
    __tablename__ = "task_calendar_form"
    form_id = Column(
        ForeignKey("form.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    task_calendar_id = Column(
        ForeignKey("task_calendar.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    form: Mapped["Form"] = relationship(back_populates="task_calendar_forms")
    task_calendar: Mapped["TaskCalendar"] = relationship(
        back_populates="task_calendar_forms"
    )


class CourtCase(TableBase, Base):
    __tablename__ = "court_case"
    client_id = Column(
        ForeignKey("client.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    client: Mapped["Client"] = relationship(back_populates="court_cases")
    court_case_forms: Mapped[List["CourtCaseForm"]] = relationship(
        back_populates="court_case"
    )
    court_case_collections: Mapped[List["CourtCaseCollection"]] = relationship(
        back_populates="court_case"
    )
    court_case_task_calendars: Mapped[List["CourtCaseTaskCalendar"]] = relationship(
        back_populates="court_case"
    )
    court_case_hearing_calendars: Mapped[
        List["CourtCaseHearingCalendar"]
    ] = relationship(back_populates="court_case")


class CourtCaseForm(TableBase, Base):
    __tablename__ = "court_case_form"
    case_id = Column(
        ForeignKey("court_case.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    form_id = Column(
        ForeignKey("form.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False
    )
    court_case: Mapped["CourtCase"] = relationship(back_populates="court_case_forms")
    form: Mapped["Form"] = relationship(back_populates="court_case_forms")


class CourtCaseCollection(TableBase, Base):
    __tablename__ = "court_case_collection"
    case_id = Column(
        ForeignKey("court_case.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    collection_id = Column(
        ForeignKey("collection.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case: Mapped["CourtCase"] = relationship(
        back_populates="court_case_collections"
    )
    collection: Mapped["Collection"] = relationship(
        back_populates="court_case_collections"
    )


class CourtCaseTaskCalendar(TableBase, Base):
    __tablename__ = "court_case_task_calendar"
    case_id = Column(
        ForeignKey("court_case.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    task_calendar_id = Column(
        ForeignKey("task_calendar.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case: Mapped["CourtCase"] = relationship(
        back_populates="court_case_task_calendars"
    )
    task_calendar: Mapped["TaskCalendar"] = relationship(
        back_populates="court_case_task_calendars"
    )


class CourtCaseHearingCalendar(TableBase, Base):
    __tablename__ = "court_case_hearing_calendar"
    case_id = Column(
        ForeignKey("court_case.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    hearing_calendar_id = Column(
        ForeignKey("hearing_calendar.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    court_case: Mapped["CourtCase"] = relationship(
        back_populates="court_case_hearing_calendars"
    )
    hearing_calendar: Mapped["HearingCalendar"] = relationship(
        back_populates="court_case_hearing_calendars"
    )
