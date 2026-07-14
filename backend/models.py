"""
BlackCat AI CMS - Database Models

This module defines all SQLAlchemy ORM models for the BlackCat AI CMS database.
Each model represents a table in the database and includes relationships to other models.

Models:
- User: Authentication and user management
- Idea: Content ideas storage (Idea Vault)
- Pattern: Writing patterns extracted from viral content
- Series: Content series with auto-numbering
- Template: Post templates for different platforms
- Audio: Audio recommendations with mood/genre tags
- Caption: Generated captions with variations
- Post: Main content posts with scheduling
- Analytics: Performance metrics tracking
- Experiment: A/B testing management
- Research: Scraped content from external sources
- Source: External content sources configuration

Version: 0.1.0
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Base class for all ORM models
Base = declarative_base()


class User(Base):
    """User model for authentication and ownership."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    google_id = Column(String, unique=True, index=True, nullable=True)  # For OAuth
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships with cascade delete
    ideas = relationship("Idea", back_populates="user", cascade="all, delete-orphan")
    series = relationship("Series", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="user", cascade="all, delete-orphan")


class Idea(Base):
    """Idea Vault - Store content ideas, quotes, observations."""
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(100), nullable=False)  # e.g., "Black Cat Files"
    text = Column(Text, nullable=False)
    source = Column(String(50), nullable=True)  # Reddit, Twitter, Book, etc.
    source_url = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    status = Column(String(20), default="active")  # active, archived, used
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="ideas")


class Pattern(Base):
    """Pattern Analyzer - Store extracted writing patterns from viral content."""
    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "Expectation Twist"
    description = Column(Text, nullable=True)
    structure = Column(Text, nullable=True)  # JSON structure of the pattern
    example_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")


class Series(Base):
    """Series Manager - Organize content into themed series with auto-numbering."""
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "Black Cat Files"
    description = Column(Text, nullable=True)
    prefix = Column(String(20), nullable=True)  # e.g., "FILE #"
    current_number = Column(Integer, default=1, nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="series")
    template = relationship("Template", back_populates="series")


class Template(Base):
    """Template Engine - Store post templates for different platforms."""
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # instagram_reel, carousel, story, png, mp4
    config = Column(Text, nullable=True)  # JSON configuration
    thumbnail = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    series = relationship("Series", back_populates="template", uselist=False)


class Audio(Base):
    """Audio Recommendation - Store audio suggestions with mood/genre tags."""
    __tablename__ = "audio"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    artist = Column(String(100), nullable=True)
    mood = Column(String(50), nullable=True)  # Calm, Funny, Sarcastic, Dark, Motivational
    genre = Column(String(50), nullable=True)  # Lo-fi, Jazz, Old songs, Ambient
    audio_url = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    is_trending = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")


class Caption(Base):
    """Caption Generator - Store generated caption variations."""
    __tablename__ = "captions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    length = Column(String(20), nullable=True)  # short, medium, long
    text = Column(Text, nullable=False)
    keywords = Column(String(500), nullable=True)  # Comma-separated
    emojis = Column(String(200), nullable=True)  # Comma-separated
    cta = Column(String(200), nullable=True)  # Call to action
    hashtags = Column(String(500), nullable=True)  # Comma-separated
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    post = relationship("Post", back_populates="captions")


class Post(Base):
    """Post - Main content entity with scheduling and platform support."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=True)
    content_type = Column(String(50), nullable=False)  # reel, carousel, story, tweet, thread
    text_content = Column(Text, nullable=True)
    asset_path = Column(String(500), nullable=True)  # Path to generated asset
    caption = Column(Text, nullable=True)
    hashtags = Column(String(500), nullable=True)
    status = Column(String(20), default="draft", nullable=False)  # draft, scheduled, published, archived
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    platform = Column(String(50), nullable=True)  # instagram, threads, linkedin, x
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="posts")
    series = relationship("Series", back_populates="posts", uselist=False)
    template = relationship("Template", back_populates="posts", uselist=False)
    idea = relationship("Idea", back_populates="posts", uselist=False)
    captions = relationship("Caption", back_populates="post", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="post", uselist=False, cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="post")


class Analytics(Base):
    """Analytics Dashboard - Track post performance metrics."""
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), unique=True, nullable=False)
    views = Column(Integer, default=0, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    comments = Column(Integer, default=0, nullable=False)
    shares = Column(Integer, default=0, nullable=False)
    saves = Column(Integer, default=0, nullable=False)
    watch_time = Column(Integer, default=0, nullable=False)  # in seconds
    followers_gained = Column(Integer, default=0, nullable=False)
    engagement_rate = Column(Float, default=0.0, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="analytics")


class Experiment(Base):
    """Experiment Manager - A/B testing for content optimization."""
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    name = Column(String(200), nullable=False)  # e.g., "Cat GIF vs Dog GIF"
    variant_a = Column(String(500), nullable=False)
    variant_b = Column(String(500), nullable=False)
    winner = Column(String(20), nullable=True)  # variant_a, variant_b, tie, null
    metric = Column(String(50), nullable=True)  # views, likes, engagement_rate, etc.
    status = Column(String(20), default="running", nullable=False)  # running, completed
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="experiments")
    post = relationship("Post", back_populates="experiments")


class Research(Base):
    """Research - Store scraped content from external sources."""
    __tablename__ = "research"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source = Column(String(50), nullable=False)  # reddit, twitter, youtube, book
    url = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    extracted_patterns = Column(Text, nullable=True)  # JSON of extracted patterns
    status = Column(String(20), default="pending", nullable=False)  # pending, processed, failed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")


class Source(Base):
    """Source - Configuration for external content sources."""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)  # subreddit, twitter_account, youtube_channel, book
    url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_scraped = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
