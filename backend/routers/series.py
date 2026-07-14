from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Series

router = APIRouter(prefix="/series", tags=["series"])


@router.post("/", response_model=schemas.SeriesResponse)
def create_series(series: schemas.SeriesCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new content series"""
    db_series = Series(**series.dict(), user_id=user_id)
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series


@router.get("/", response_model=List[schemas.SeriesResponse])
def get_series(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all series for the user"""
    series_list = db.query(Series).filter(Series.user_id == user_id).offset(skip).limit(limit).all()
    return series_list


@router.get("/{series_id}", response_model=schemas.SeriesResponse)
def get_series_by_id(series_id: int, db: Session = Depends(get_db)):
    """Get a specific series by ID"""
    series = db.query(Series).filter(Series.id == series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series


@router.put("/{series_id}", response_model=schemas.SeriesResponse)
def update_series(series_id: int, series_update: dict, db: Session = Depends(get_db)):
    """Update a series"""
    db_series = db.query(Series).filter(Series.id == series_id).first()
    if not db_series:
        raise HTTPException(status_code=404, detail="Series not found")
    
    for key, value in series_update.items():
        setattr(db_series, key, value)
    
    db.commit()
    db.refresh(db_series)
    return db_series


@router.delete("/{series_id}")
def delete_series(series_id: int, db: Session = Depends(get_db)):
    """Delete a series"""
    db_series = db.query(Series).filter(Series.id == series_id).first()
    if not db_series:
        raise HTTPException(status_code=404, detail="Series not found")
    
    db.delete(db_series)
    db.commit()
    return {"message": "Series deleted successfully"}
