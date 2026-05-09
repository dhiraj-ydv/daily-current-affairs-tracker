from pydantic import BaseModel
from typing import Optional

class DailyStatusBase(BaseModel):
    date: str
    status: str

class DailyStatusCreate(DailyStatusBase):
    pass

class DailyStatusUpdate(BaseModel):
    status: Optional[str] = None

class DailyStatus(DailyStatusBase):
    id: int

    class Config:
        from_attributes = True
