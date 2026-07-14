from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
from models import Analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/", response_model=schemas.AnalyticsResponse)
def create_analytics(analytics: schemas.AnalyticsCreate, db: Session = Depends(get_db)):
    """Create analytics for a post"""
    db_analytics = Analytics(**analytics.dict())
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    return db_analytics


@router.get("/post/{post_id}", response_model=schemas.AnalyticsResponse)
def get_analytics_for_post(post_id: int, db: Session = Depends(get_db)):
    """Get analytics for a specific post"""
    analytics = db.query(Analytics).filter(Analytics.post_id == post_id).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")
    return analytics


@router.put("/post/{post_id}", response_model=schemas.AnalyticsResponse)
def update_analytics(post_id: int, analytics_update: dict, db: Session = Depends(get_db)):
    """Update analytics for a post"""
    db_analytics = db.query(Analytics).filter(Analytics.post_id == post_id).first()
    if not db_analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")
    
    for key, value in analytics_update.items():
        setattr(db_analytics, key, value)
    
    db.commit()
    db.refresh(db_analytics)
    return db_analytics


@router.get("/summary", response_model=dict)
def get_analytics_summary(db: Session = Depends(get_db), user_id: int = 1):
    """Get overall analytics summary"""
    from models import Post
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    
    total_views = 0
    total_likes = 0
    total_comments = 0
    total_shares = 0
    total_saves = 0
    
    for post in posts:
        if post.analytics:
            total_views += post.analytics.views or 0
            total_likes += post.analytics.likes or 0
            total_comments += post.analytics.comments or 0
            total_shares += post.analytics.shares or 0
            total_saves += post.analytics.saves or 0
    
    return {
        "total_posts": len(posts),
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_saves": total_saves,
        "average_engagement_rate": sum(p.analytics.engagement_rate for p in posts if p.analytics) / len(posts) if posts else 0
    }
