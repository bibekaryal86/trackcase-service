import datetime
from typing import Optional

from pydantic import BaseModel


class BaseModelSchema(BaseModel):
    id: Optional[int] = 0
    created: Optional[datetime.datetime] = None
    modified: Optional[datetime.datetime] = None


class ResponseBase(BaseModel):
    delete_count: Optional[int] = 0
    msg: Optional[str] = None
    err_msg: Optional[str] = None


# judge
class JudgeBase:
    name: str
    webex: Optional[str] = None
    court_id: int


class Judge(JudgeBase, BaseModelSchema):
    class Config:
        orm_mode = True


class JudgeRequest(JudgeBase, BaseModelSchema):
    pass


class JudgeResponse(ResponseBase):
    judges: list[Judge] = []


# court
class CourtBase:
    name: str
    address: str
    dhs_address: str


class Court(CourtBase, BaseModelSchema):
    judges: list[Judge] = []

    class Config:
        orm_mode = True


class CourtRequest(CourtBase, BaseModelSchema):
    pass


class CourtResponse(ResponseBase):
    courts: list[Court] = []
