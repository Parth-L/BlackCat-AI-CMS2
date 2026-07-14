from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    google_id: Optional[str] = None


class UserResponse(UserBase):
    id: int
    google_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IdeaBase(BaseModel):
    category: str
    text: str
    source: Optional[str] = None
    source_url: Optional[str] = None
    tags: Optional[str] = None


class IdeaCreate(IdeaBase):
    pass


class IdeaResponse(IdeaBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PatternBase(BaseModel):
    name: str
    description: Optional[str] = None
    structure: Optional[str] = None
    example_content: Optional[str] = None


class PatternCreate(PatternBase):
    pass


class PatternResponse(PatternBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SeriesBase(BaseModel):
    name: str
    description: Optional[str] = None
    prefix: Optional[str] = None
    template_id: Optional[int] = None


class SeriesCreate(SeriesBase):
    pass


class SeriesResponse(SeriesBase):
    id: int
    user_id: int
    current_number: int
    created_at: datetime

    class Config:
        from_attributes = True


class TemplateBase(BaseModel):
    name: str
    type: str
    config: str
    thumbnail: Optional[str] = None


class TemplateCreate(TemplateBase):
    pass


class TemplateResponse(TemplateBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AudioBase(BaseModel):
    title: str
    artist: Optional[str] = None
    mood: Optional[str] = None
    genre: Optional[str] = None
    audio_url: Optional[str] = None
    duration: Optional[int] = None
    is_trending: bool = False


class AudioCreate(AudioBase):
    pass


class AudioResponse(AudioBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CaptionBase(BaseModel):
    length: str
    text: str
    keywords: Optional[str] = None
    emojis: Optional[str] = None
    cta: Optional[str] = None
    hashtags: Optional[str] = None


class CaptionCreate(CaptionBase):
    post_id: Optional[int] = None


class CaptionResponse(CaptionBase):
    id: int
    user_id: int
    post_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    content_type: str
    text_content: Optional[str] = None
    caption: Optional[str] = None
    hashtags: Optional[str] = None
    platform: Optional[str] = None
    series_id: Optional[int] = None
    template_id: Optional[int] = None
    idea_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    asset_path: Optional[str] = None


class PostResponse(PostBase):
    id: int
    user_id: int
    asset_path: Optional[str] = None
    status: str
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnalyticsBase(BaseModel):
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    watch_time: int = 0
    followers_gained: int = 0
    engagement_rate: float = 0.0


class AnalyticsCreate(AnalyticsBase):
    post_id: int


class AnalyticsResponse(AnalyticsBase):
    id: int
    post_id: int
    last_updated: datetime

    class Config:
        from_attributes = True


class ExperimentBase(BaseModel):
    name: str
    variant_a: str
    variant_b: str
    metric: Optional[str] = None
    post_id: int


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentResponse(ExperimentBase):
    id: int
    user_id: int
    winner: Optional[str] = None
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ResearchBase(BaseModel):
    source: str
    url: Optional[str] = None
    content: Optional[str] = None
    extracted_patterns: Optional[str] = None


class ResearchCreate(ResearchBase):
    pass


class ResearchResponse(ResearchBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    name: str
    type: str
    url: Optional[str] = None
    is_active: bool = True


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: int
    user_id: int
    last_scraped: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
