from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Idea

router = APIRouter(tags=["ideas"])  # Removed prefix - handled in main.py


@router.post("/ideas/", response_model=schemas.IdeaResponse)
def create_idea(idea: schemas.IdeaCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new idea (Phase 1: hardcoded user_id=1)"""
    db_idea = Idea(**idea.dict(), user_id=user_id)
    db.add(db_idea)
    db.commit()
    db.refresh(db_idea)
    return db_idea


@router.get("/ideas/", response_model=List[schemas.IdeaResponse])
def get_ideas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all ideas for the user"""
    ideas = db.query(Idea).filter(Idea.user_id == user_id).offset(skip).limit(limit).all()
    return ideas


@router.get("/ideas/{idea_id}", response_model=schemas.IdeaResponse)
def get_idea(idea_id: int, db: Session = Depends(get_db)):
    """Get a specific idea by ID"""
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea


@router.put("/ideas/{idea_id}", response_model=schemas.IdeaResponse)
def update_idea(idea_id: int, idea_update: dict, db: Session = Depends(get_db)):
    """Update an idea"""
    db_idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not db_idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    for key, value in idea_update.items():
        setattr(db_idea, key, value)
    
    db.commit()
    db.refresh(db_idea)
    return db_idea


@router.delete("/ideas/{idea_id}")
def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    """Delete an idea"""
    db_idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not db_idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    db.delete(db_idea)
    db.commit()
    return {"message": "Idea deleted successfully"}
