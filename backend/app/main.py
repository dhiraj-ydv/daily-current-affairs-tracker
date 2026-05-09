from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration for Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/statuses/", response_model=List[schemas.DailyStatus])
def read_statuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    statuses = crud.get_daily_statuses(db, skip=skip, limit=limit)
    return statuses

@app.get("/statuses/{date}", response_model=schemas.DailyStatus)
def read_status_by_date(date: str, db: Session = Depends(get_db)):
    db_status = crud.get_daily_status_by_date(db, date=date)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status

@app.post("/statuses/", response_model=schemas.DailyStatus)
def create_status(status: schemas.DailyStatusCreate, db: Session = Depends(get_db)):
    db_status = crud.get_daily_status_by_date(db, date=status.date)
    if db_status:
        # If exists, update instead of error? Or error?
        # Let's update if exists for better UX
        return crud.update_daily_status(db=db, date=status.date, daily_status=schemas.DailyStatusUpdate(status=status.status))
    return crud.create_daily_status(db=db, daily_status=status)

@app.put("/statuses/{date}", response_model=schemas.DailyStatus)
def update_status(date: str, status: schemas.DailyStatusUpdate, db: Session = Depends(get_db)):
    db_status = crud.update_daily_status(db=db, date=date, daily_status=status)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status

@app.delete("/statuses/{date}")
def delete_status(date: str, db: Session = Depends(get_db)):
    db_status = crud.delete_daily_status(db=db, date=date)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return {"message": "Successfully deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
