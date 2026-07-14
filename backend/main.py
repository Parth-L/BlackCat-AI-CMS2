"""
BlackCat AI CMS - Main Application Entry Point

This module initializes the FastAPI application, configures middleware,
and registers all API routers for the content management system.

Version: 0.1.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine  # Database connection engine
from routers import ideas, posts, series, analytics, experiments, assets  # API routers
from models import Base  # SQLAlchemy base model

# Initialize FastAPI application with metadata
app = FastAPI(
    title="BlackCat AI CMS",
    description="AI-Powered Content Research, Creation & Publishing Platform",
    version="0.1.0",  # Updated to match git tag
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",  # ReDoc endpoint
    openapi_url="/openapi.json"  # OpenAPI schema endpoint
)

# Configure CORS middleware for frontend communication
# NOTE: In production, restrict allow_origins to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register all API routers
# Each router handles a specific domain/module of the application
# NOTE: Routers now include full paths, so no prefix is needed here
app.include_router(ideas.router, tags=["Ideas"])
app.include_router(posts.router, tags=["Posts"])
app.include_router(series.router, tags=["Series"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(experiments.router, tags=["Experiments"])
app.include_router(assets.router, tags=["Assets"])


@app.on_event("startup")
async def startup_event():
    """
    Initialize database on application startup.
    
    This event handler creates all database tables defined in models.py
    if they don't already exist. Runs automatically when the server starts.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - Returns application information.
    
    Returns:
        dict: Application name, version, and documentation URL
    """
    return {
        "message": "Welcome to BlackCat AI CMS",
        "version": "0.1.0",
        "description": "AI-Powered Content Research, Creation & Publishing Platform",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        dict: Simple status indicator
    """
    return {"status": "healthy"}
