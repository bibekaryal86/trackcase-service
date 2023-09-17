from typing import Any, List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
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


class FormStatus(TableBase, Base):
    __tablename__ = "form_status"
    name: str = Column(String(25), unique=True, nullable=False)
    description: str = Column(String(280), nullable=False)


class CollectionMethod(TableBase, Base):
    __tablename__ = "collection_method"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)


class HearingType(TableBase, Base):
    __tablename__ = "hearing_type"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)


class TaskType(TableBase, Base):
    __tablename__ = "task_type"
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(280), nullable=False)


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
    parent: Mapped[Court] = relationship(back_populates="judges")
