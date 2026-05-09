from sqlalchemy import Column, Integer, String, Date
from .database import Base

class DailyStatus(Base):
    __tablename__ = "daily_status"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True) # Storing as YYYY-MM-DD string for simplicity
    status = Column(String)
