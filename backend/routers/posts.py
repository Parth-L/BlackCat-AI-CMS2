from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Post

router = APIRouter(tags=["posts"])  # Removed prefix - handled in main.py


@router.post("/posts/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new post"""
    db_post = Post(**post.dict(), user_id=user_id, status="draft")
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/posts/", response_model=List[schemas.PostResponse])
def get_posts(skip: int = 0, limit: int = 100, platform: str = None, db: Session = Depends(get_db), user_id: int = 1):
    """Get all posts for the user, optionally filtered by platform"""
    query = db.query(Post).filter(Post.user_id == user_id)
    if platform:
        query = query.filter(Post.platform == platform)
    posts = query.offset(skip).limit(limit).all()
    return posts


@router.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
    """Update a post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = post_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}


@router.post("/posts/{post_id}/schedule", response_model=schemas.PostResponse)
def schedule_post(post_id: int, schedule_data: dict, db: Session = Depends(get_db)):
    """Schedule a post for publishing"""
    from datetime import datetime
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    scheduled_time = schedule_data.get("scheduled_time")
    if scheduled_time:
        try:
            db_post.scheduled_time = datetime.fromisoformat(scheduled_time)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format. Use ISO 8601 format (e.g., 2024-12-25T10:00:00)")
    
    db_post.status = "scheduled"
    db.commit()
    db.refresh(db_post)
    return db_post
