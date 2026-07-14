from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Template, Audio

router = APIRouter(tags=["assets"])  # Removed prefix - handled in main.py


# Template endpoints
@router.post("/assets/templates/", response_model=schemas.TemplateResponse)
def create_template(template: schemas.TemplateCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new content template"""
    db_template = Template(**template.dict(), user_id=user_id)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.get("/assets/templates/", response_model=List[schemas.TemplateResponse])
def get_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all templates for the user"""
    templates = db.query(Template).filter(Template.user_id == user_id).offset(skip).limit(limit).all()
    return templates


@router.get("/assets/templates/{template_id}", response_model=schemas.TemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    """Get a specific template by ID"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.delete("/assets/templates/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    """Delete a template"""
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Template not found")

    db.delete(db_template)
    db.commit()
    return {"message": "Template deleted successfully"}


# Audio endpoints
@router.post("/assets/audio/", response_model=schemas.AudioResponse)
def create_audio(audio: schemas.AudioCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Add a new audio track"""
    db_audio = Audio(**audio.dict(), user_id=user_id)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


@router.get("/assets/audio/", response_model=List[schemas.AudioResponse])
def get_audio_tracks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all audio tracks for the user"""
    audio_tracks = db.query(Audio).filter(Audio.user_id == user_id).offset(skip).limit(limit).all()
    return audio_tracks


@router.get("/assets/audio/trending/", response_model=List[schemas.AudioResponse])
def get_trending_audio(db: Session = Depends(get_db)):
    """Get trending audio recommendations"""
    # In production, this would fetch from external API
    audio_tracks = db.query(Audio).filter(Audio.is_trending == True).limit(20).all()
    return audio_tracks


@router.get("/assets/audio/{audio_id}", response_model=schemas.AudioResponse)
def get_audio_track(audio_id: int, db: Session = Depends(get_db)):
    """Get a specific audio track by ID"""
    audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio track not found")
    return audio


@router.delete("/assets/audio/{audio_id}")
def delete_audio_track(audio_id: int, db: Session = Depends(get_db)):
    """Delete an audio track"""
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if not db_audio:
        raise HTTPException(status_code=404, detail="Audio track not found")

    db.delete(db_audio)
    db.commit()
    return {"message": "Audio track deleted successfully"}
