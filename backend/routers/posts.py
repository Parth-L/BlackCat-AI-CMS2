from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = 1):
    """Create a new post"""
    db_post = Post(**post.dict(), user_id=user_id, status="draft")
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = 1):
    """Get all posts for the user"""
    posts = db.query(Post).filter(Post.user_id == user_id).offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.PostResponse)
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


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}
