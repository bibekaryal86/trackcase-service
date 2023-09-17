import datetime
from typing import Optional

from pydantic import BaseModel


class SchemaBase(BaseModel):
    id: Optional[int]
    created: Optional[datetime.datetime]
    modified: Optional[datetime.datetime]


class Judge(SchemaBase):
    name: str
    webex: Optional[str]
    court_id: int

    class Config:
        orm_mode = True
        # from_attributes = True


class Court(SchemaBase):
    name: str
    address: str
    dhs_address: Optional[str]
    judges: list[Judge] = []

    class Config:
        orm_mode = True
        # from_attributes=True
