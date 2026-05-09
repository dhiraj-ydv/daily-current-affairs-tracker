from sqlalchemy.orm import Session
from . import models, schemas

def get_daily_status(db: Session, status_id: int):
    return db.query(models.DailyStatus).filter(models.DailyStatus.id == status_id).first()

def get_daily_status_by_date(db: Session, date: str):
    return db.query(models.DailyStatus).filter(models.DailyStatus.date == date).first()

def get_daily_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DailyStatus).order_by(models.DailyStatus.date.desc()).offset(skip).limit(limit).all()

def create_daily_status(db: Session, daily_status: schemas.DailyStatusCreate):
    db_daily_status = models.DailyStatus(
        date=daily_status.date, 
        status=daily_status.status,
        sources=daily_status.sources or "",
        key_topics=daily_status.key_topics or "",
        remark=daily_status.remark or ""
    )
    db.add(db_daily_status)
    db.commit()
    db.refresh(db_daily_status)
    return db_daily_status

def update_daily_status(db: Session, date: str, daily_status: schemas.DailyStatusUpdate):
    db_daily_status = db.query(models.DailyStatus).filter(models.DailyStatus.date == date).first()
    if db_daily_status:
        if daily_status.status is not None:
            db_daily_status.status = daily_status.status
        if daily_status.sources is not None:
            db_daily_status.sources = daily_status.sources
        if daily_status.key_topics is not None:
            db_daily_status.key_topics = daily_status.key_topics
        if daily_status.remark is not None:
            db_daily_status.remark = daily_status.remark
        db.commit()
        db.refresh(db_daily_status)
    return db_daily_status

def delete_daily_status(db: Session, date: str):
    db_daily_status = db.query(models.DailyStatus).filter(models.DailyStatus.date == date).first()
    if db_daily_status:
        db.delete(db_daily_status)
        db.commit()
    return db_daily_status
