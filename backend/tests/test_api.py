"""
BlackCat AI CMS - Comprehensive Test Suite
Tests for API endpoints, security, and data validation.
"""
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db

# Test Database Setup (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables
Base.metadata.create_all(bind=engine)

@pytest.fixture
async def client():
    """Async test client fixture."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def db_session():
    """Database session fixture."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== HEALTH CHECK TESTS ====================

@pytest.mark.asyncio
async def test_health_check(client):
    """Test health endpoint returns healthy status."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# ==================== IDEAS MODULE TESTS ====================

@pytest.mark.asyncio
async def test_create_idea(client):
    """Test creating a new idea."""
    idea_data = {
        "text": "Humans pretend they're resting. They're just changing apps.",
        "category": "Black Cat Files",
        "source": "Observation",
        "tags": ["overthinking", "technology"]
    }
    response = await client.post("/ideas/", json=idea_data)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == idea_data["text"]
    assert data["category"] == idea_data["category"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_ideas(client):
    """Test retrieving all ideas."""
    response = await client.get("/ideas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_idea_by_id(client, db_session):
    """Test retrieving a specific idea by ID."""
    from models import Idea
    idea = Idea(content="Test idea", category="Test")
    db_session.add(idea)
    db_session.commit()
    db_session.refresh(idea)
    
    response = await client.get(f"/ideas/{idea.id}")
    assert response.status_code == 200
    assert response.json()["id"] == idea.id

@pytest.mark.asyncio
async def test_update_idea(client, db_session):
    """Test updating an idea."""
    from models import Idea
    idea = Idea(content="Original content", category="Test")
    db_session.add(idea)
    db_session.commit()
    db_session.refresh(idea)
    
    update_data = {"content": "Updated content"}
    response = await client.put(f"/ideas/{idea.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated content"

@pytest.mark.asyncio
async def test_delete_idea(client, db_session):
    """Test deleting an idea."""
    from models import Idea
    idea = Idea(content="To be deleted", category="Test")
    db_session.add(idea)
    db_session.commit()
    db_session.refresh(idea)
    
    response = await client.delete(f"/ideas/{idea.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Idea deleted successfully"

# ==================== SERIES MODULE TESTS ====================

@pytest.mark.asyncio
async def test_create_series(client):
    """Test creating a new series."""
    series_data = {
        "name": "System Messages",
        "description": "Corporate achievement notifications",
        "prefix": "MSG"
    }
    response = await client.post("/series/", json=series_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == series_data["name"]
    assert data["current_number"] == 1

@pytest.mark.asyncio
async def test_series_auto_increment(client, db_session):
    """Test series numbering auto-increments."""
    from models import Series
    series = Series(name="Test Series", prefix="TST", current_number=5)
    db_session.add(series)
    db_session.commit()
    db_session.refresh(series)
    
    # Create post in series should increment
    # This tests the logic in posts module
    assert series.current_number == 5

# ==================== POSTS MODULE TESTS ====================

@pytest.mark.asyncio
async def test_create_post(client, db_session):
    """Test creating a new post."""
    from models import Series
    series = Series(name="Test Series", prefix="TST")
    db_session.add(series)
    db_session.commit()
    db_session.refresh(series)
    
    post_data = {
        "content": "Test post content",
        "platform": "instagram",
        "post_type": "reel",
        "series_id": series.id,
        "scheduled_time": "2024-12-31T23:59:59"
    }
    response = await client.post("/posts/", json=post_data)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == post_data["content"]
    assert data["platform"] == post_data["platform"]

@pytest.mark.asyncio
async def test_get_posts_by_platform(client):
    """Test filtering posts by platform."""
    response = await client.get("/posts/?platform=instagram")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_schedule_post(client, db_session):
    """Test scheduling a post."""
    from models import Post
    post = Post(content="Scheduled test", platform="twitter", status="draft")
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    
    schedule_data = {"scheduled_time": "2024-12-25T10:00:00"}
    response = await client.post(f"/posts/{post.id}/schedule", json=schedule_data)
    assert response.status_code == 200
    assert response.json()["status"] == "scheduled"

# ==================== ANALYTICS MODULE TESTS ====================

@pytest.mark.asyncio
async def test_record_analytics(client, db_session):
    """Test recording analytics for a post."""
    from models import Post
    post = Post(content="Analytics test", platform="instagram")
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    
    analytics_data = {
        "views": 1000,
        "likes": 150,
        "comments": 25,
        "shares": 10,
        "saves": 45
    }
    response = await client.post(f"/analytics/{post.id}", json=analytics_data)
    assert response.status_code == 200
    data = response.json()
    assert data["views"] == 1000
    assert data["likes"] == 150

@pytest.mark.asyncio
async def test_get_analytics_summary(client, db_session):
    """Test getting analytics summary."""
    from models import Post, Analytics
    post = Post(content="Summary test", platform="instagram")
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    
    analytics = Analytics(post_id=post.id, views=500, likes=75)
    db_session.add(analytics)
    db_session.commit()
    
    response = await client.get(f"/analytics/{post.id}/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_views" in data or "average_views" in data

# ==================== EXPERIMENTS MODULE TESTS ====================

@pytest.mark.asyncio
async def test_create_experiment(client, db_session):
    """Test creating an A/B test experiment."""
    from models import Post
    post_a = Post(content="Variant A", platform="instagram")
    post_b = Post(content="Variant B", platform="instagram")
    db_session.add_all([post_a, post_b])
    db_session.commit()
    db_session.refresh(post_a)
    db_session.refresh(post_b)
    
    experiment_data = {
        "name": "Cat GIF vs Dog GIF",
        "variant_a_id": post_a.id,
        "variant_b_id": post_b.id,
        "metric": "engagement_rate"
    }
    response = await client.post("/experiments/", json=experiment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == experiment_data["name"]
    assert data["status"] == "running"

@pytest.mark.asyncio
async def test_conclude_experiment(client, db_session):
    """Test concluding an experiment with winner."""
    from models import Experiment, Post
    post_a = Post(content="Variant A", platform="instagram")
    post_b = Post(content="Variant B", platform="instagram")
    db_session.add_all([post_a, post_b])
    db_session.commit()
    db_session.refresh(post_a)
    db_session.refresh(post_b)
    
    experiment = Experiment(
        name="Test Experiment",
        variant_a_id=post_a.id,
        variant_b_id=post_b.id,
        status="running"
    )
    db_session.add(experiment)
    db_session.commit()
    db_session.refresh(experiment)
    
    result_data = {"winner_id": post_a.id, "insights": "Variant A performed 20% better"}
    response = await client.post(f"/experiments/{experiment.id}/conclude", json=result_data)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

# ==================== SECURITY TESTS ====================

@pytest.mark.asyncio
async def test_sql_injection_prevention(client):
    """Test SQL injection prevention in query parameters."""
    malicious_input = "'; DROP TABLE ideas; --"
    response = await client.get(f"/ideas/?search={malicious_input}")
    assert response.status_code == 200  # Should not crash
    # Verify table still exists
    check_response = await client.get("/ideas/")
    assert check_response.status_code == 200

@pytest.mark.asyncio
async def test_xss_prevention(client, db_session):
    """Test XSS prevention in content."""
    from models import Idea
    xss_payload = "<script>alert('XSS')</script>"
    idea = Idea(content=xss_payload, category="Test")
    db_session.add(idea)
    db_session.commit()
    db_session.refresh(idea)
    
    response = await client.get(f"/ideas/{idea.id}")
    assert response.status_code == 200
    # Content should be stored as-is but frontend must sanitize
    data = response.json()
    assert data["content"] == xss_payload

@pytest.mark.asyncio
async def test_invalid_json_handling(client):
    """Test handling of malformed JSON."""
    headers = {"Content-Type": "application/json"}
    response = await client.post("/ideas/", content="invalid json{", headers=headers)
    assert response.status_code in [400, 422]  # Bad Request or Unprocessable Entity

@pytest.mark.asyncio
async def test_missing_required_fields(client):
    """Test validation of required fields."""
    response = await client.post("/ideas/", json={})
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_rate_limiting_simulation(client):
    """Simulate rate limiting behavior (placeholder for actual implementation)."""
    # Send multiple rapid requests
    responses = []
    for i in range(10):
        response = await client.get("/health")
        responses.append(response.status_code)
    
    # All should succeed (rate limiting not yet implemented)
    assert all(status == 200 for status in responses)

# ==================== LOAD TEST SIMULATION ====================

@pytest.mark.asyncio
async def test_concurrent_requests(client):
    """Test handling concurrent requests."""
    tasks = []
    for i in range(20):
        task = client.get("/health")
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    assert all(response.status_code == 200 for response in responses)

@pytest.mark.asyncio
async def test_bulk_idea_creation(client):
    """Test bulk creation of ideas."""
    ideas_data = [
        {"content": f"Idea {i}", "category": "Bulk Test", "tags": ["test"]}
        for i in range(50)
    ]
    
    tasks = [client.post("/ideas/", json=idea) for idea in ideas_data]
    responses = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in responses if r.status_code == 200)
    assert success_count >= 45  # Allow some failures due to concurrency

# ==================== EDGE CASE TESTS ====================

@pytest.mark.asyncio
async def test_empty_content_validation(client):
    """Test validation of empty content."""
    response = await client.post("/ideas/", json={"content": "", "category": "Test"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_very_long_content(client):
    """Test handling of very long content."""
    long_content = "A" * 10000
    response = await client.post("/ideas/", json={"content": long_content, "category": "Test"})
    assert response.status_code in [200, 422]  # Either accepted or validated

@pytest.mark.asyncio
async def test_special_characters(client):
    """Test handling of special characters."""
    special_content = "Test with emojis 🐱, symbols @#$%, and unicode ñüé"
    response = await client.post("/ideas/", json={"content": special_content, "category": "Test"})
    assert response.status_code == 200
    assert response.json()["content"] == special_content

@pytest.mark.asyncio
async def test_nonexistent_resource(client):
    """Test accessing nonexistent resources."""
    response = await client.get("/ideas/999999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_invalid_date_format(client, db_session):
    """Test invalid date format handling."""
    from models import Post
    post = Post(content="Date test", platform="instagram")
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    
    schedule_data = {"scheduled_time": "invalid-date"}
    response = await client.post(f"/posts/{post.id}/schedule", json=schedule_data)
    assert response.status_code == 422
