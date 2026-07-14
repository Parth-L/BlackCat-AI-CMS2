from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Experiment

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("/", response_model=schemas.ExperimentResponse)
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new A/B test experiment"""
    db_experiment = Experiment(**experiment.dict(), user_id=user_id)
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


@router.get("/", response_model=List[schemas.ExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all experiments for the user"""
    experiments = db.query(Experiment).filter(Experiment.user_id == user_id).offset(skip).limit(limit).all()
    return experiments


@router.get("/{experiment_id}", response_model=schemas.ExperimentResponse)
def get_experiment(experiment_id: int, db: Session = Depends(get_db)):
    """Get a specific experiment by ID"""
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@router.put("/{experiment_id}/result", response_model=schemas.ExperimentResponse)
def set_experiment_result(experiment_id: int, winner: str, db: Session = Depends(get_db)):
    """Set the winner of an experiment"""
    db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    from datetime import datetime
    db_experiment.winner = winner
    db_experiment.status = "completed"
    db_experiment.ended_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


@router.delete("/{experiment_id}")
def delete_experiment(experiment_id: int, db: Session = Depends(get_db)):
    """Delete an experiment"""
    db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    db.delete(db_experiment)
    db.commit()
    return {"message": "Experiment deleted successfully"}
