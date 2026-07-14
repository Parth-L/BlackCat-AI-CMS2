from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Experiment

router = APIRouter(tags=["experiments"])  # Removed prefix - handled in main.py


@router.post("/experiments/", response_model=schemas.ExperimentResponse)
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new A/B test experiment"""
    db_experiment = Experiment(**experiment.dict(), user_id=user_id, status="running")
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


@router.get("/experiments/", response_model=List[schemas.ExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all experiments for the user"""
    experiments = db.query(Experiment).filter(Experiment.user_id == user_id).offset(skip).limit(limit).all()
    return experiments


@router.get("/experiments/{experiment_id}", response_model=schemas.ExperimentResponse)
def get_experiment(experiment_id: int, db: Session = Depends(get_db)):
    """Get a specific experiment by ID"""
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@router.post("/experiments/{experiment_id}/conclude", response_model=schemas.ExperimentResponse)
def conclude_experiment(experiment_id: int, result_data: dict, db: Session = Depends(get_db)):
    """Conclude an experiment with results"""
    db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    db_experiment.status = "completed"
    db_experiment.winner_id = result_data.get("winner_id")
    db_experiment.insights = result_data.get("insights", "")
    
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, db: Session = Depends(get_db)):
    """Delete an experiment"""
    db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    db.delete(db_experiment)
    db.commit()
    return {"message": "Experiment deleted successfully"}
