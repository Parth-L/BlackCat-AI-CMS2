from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import schemas
from models import Template, Audio

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/templates/", response_model=schemas.TemplateResponse)
def create_template(template: schemas.TemplateCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new content template"""
    db_template = Template(**template.dict(), user_id=user_id)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.get("/templates/", response_model=List[schemas.TemplateResponse])
def get_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all templates for the user"""
    templates = db.query(Template).filter(Template.user_id == user_id).offset(skip).limit(limit).all()
    return templates


@router.get("/templates/{template_id}", response_model=schemas.TemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    """Get a specific template by ID"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.delete("/templates/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    """Delete a template"""
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    db.delete(db_template)
    db.commit()
    return {"message": "Template deleted successfully"}


@router.post("/audio/", response_model=schemas.AudioResponse)
def create_audio(audio: schemas.AudioCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Add a new audio track"""
    db_audio = Audio(**audio.dict(), user_id=user_id)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


@router.get("/audio/", response_model=List[schemas.AudioResponse])
def get_audio_tracks(skip: int = 0, limit: int = 100, mood: Optional[str] = None, 
                      db: Session = Depends(get_db), user_id: int = 1):
    """Get all audio tracks, optionally filtered by mood"""
    query = db.query(Audio).filter(Audio.user_id == user_id)
    if mood:
        query = query.filter(Audio.mood == mood)
    audio_tracks = query.offset(skip).limit(limit).all()
    return audio_tracks


@router.get("/audio/trending/", response_model=List[schemas.AudioResponse])
def get_trending_audio(limit: int = 20, db: Session = Depends(get_db), user_id: int = 1):
    """Get trending audio tracks"""
    audio_tracks = db.query(Audio).filter(
        Audio.user_id == user_id,
        Audio.is_trending == True
    ).limit(limit).all()
    return audio_tracks


@router.delete("/audio/{audio_id}")
def delete_audio(audio_id: int, db: Session = Depends(get_db)):
    """Delete an audio track"""
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if not db_audio:
        raise HTTPException(status_code=404, detail="Audio track not found")
    
    db.delete(db_audio)
    db.commit()
    return {"message": "Audio track deleted successfully"}
