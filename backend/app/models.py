from sqlalchemy import Column, Integer, String
from .database import Base

class DailyStatus(Base):
    __tablename__ = "daily_status"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True)
    status = Column(String)
    sources = Column(String, default="")
    key_topics = Column(String, default="")
    remark = Column(String, default="")
