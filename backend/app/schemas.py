from pydantic import BaseModel
from typing import Optional

class DailyStatusBase(BaseModel):
    date: str
    status: str
    sources: Optional[str] = ""
    key_topics: Optional[str] = ""
    remark: Optional[str] = ""

class DailyStatusCreate(DailyStatusBase):
    pass

class DailyStatusUpdate(BaseModel):
    status: Optional[str] = None
    sources: Optional[str] = None
    key_topics: Optional[str] = None
    remark: Optional[str] = None

class DailyStatus(DailyStatusBase):
    id: int

    class Config:
        from_attributes = True
