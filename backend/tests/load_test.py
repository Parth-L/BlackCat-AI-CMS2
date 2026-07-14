"""
BlackCat AI CMS - Load Testing Script with Locust
Simulates real-world user traffic patterns for performance testing.
"""
from locust import HttpUser, task, between, events
import random
import json

class BlackCatUser(HttpUser):
    """
    Simulates a typical BlackCat AI CMS user behavior.
    Users create ideas, manage series, schedule posts, and check analytics.
    """
    
    # Wait time between tasks (1-3 seconds)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when user starts - login or initialize session."""
        self.idea_ids = []
        self.series_ids = []
        self.post_ids = []
    
    @task(3)
    def view_health(self):
        """Lightweight health check - high frequency."""
        self.client.get("/health")
    
    @task(5)
    def list_ideas(self):
        """Browse existing ideas - common operation."""
        self.client.get("/ideas/")
    
    @task(4)
    def create_idea(self):
        """Create new content ideas - core functionality."""
        idea_data = {
            "content": f"Generated idea {random.randint(1, 1000)}",
            "category": random.choice(["Black Cat Files", "Observations", "Quotes"]),
            "source": "Test",
            "tags": ["test", "load-test"]
        }
        response = self.client.post("/ideas/", json=idea_data)
        if response.status_code == 200:
            try:
                data = response.json()
                self.idea_ids.append(data.get("id"))
            except:
                pass
    
    @task(2)
    def view_single_idea(self):
        """View a specific idea detail."""
        if self.idea_ids:
            idea_id = random.choice(self.idea_ids)
            self.client.get(f"/ideas/{idea_id}")
    
    @task(2)
    def create_series(self):
        """Create content series for organization."""
        series_data = {
            "name": f"Series {random.randint(1, 100)}",
            "description": "Load test series",
            "prefix": "LT"
        }
        response = self.client.post("/series/", json=series_data)
        if response.status_code == 200:
            try:
                data = response.json()
                self.series_ids.append(data.get("id"))
            except:
                pass
    
    @task(3)
    def list_posts(self):
        """Browse scheduled/published posts."""
        platforms = ["instagram", "twitter", "linkedin"]
        platform = random.choice(platforms)
        self.client.get(f"/posts/?platform={platform}")
    
    @task(2)
    def record_analytics(self):
        """Record performance metrics for posts."""
        if self.post_ids:
            post_id = random.choice(self.post_ids)
            analytics_data = {
                "views": random.randint(100, 10000),
                "likes": random.randint(10, 500),
                "comments": random.randint(0, 50),
                "shares": random.randint(0, 30),
                "saves": random.randint(5, 100)
            }
            self.client.post(f"/analytics/{post_id}", json=analytics_data)
    
    @task(1)
    def create_experiment(self):
        """Create A/B testing experiments - less frequent."""
        # This would require existing posts, simplified for load test
        pass
    
    @task(1)
    def view_analytics_summary(self):
        """Check analytics dashboard."""
        if self.post_ids:
            post_id = random.choice(self.post_ids)
            self.client.get(f"/analytics/{post_id}/summary")


class StressTestUser(HttpUser):
    """
    Aggressive user for stress testing - simulates power users or bots.
    """
    wait_time = between(0.1, 0.5)  # Very fast requests
    
    @task
    def rapid_health_checks(self):
        """Flood health endpoint."""
        self.client.get("/health")
    
    @task
    def rapid_idea_creation(self):
        """Rapidly create ideas to test database write performance."""
        idea_data = {
            "content": f"Stress test idea {random.randint(1, 10000)}",
            "category": "Stress Test",
            "tags": ["stress"]
        }
        self.client.post("/ideas/", json=idea_data)


# Custom event handlers for reporting
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Log slow requests for analysis."""
    if response_time > 1000:  # More than 1 second
        print(f"WARNING: Slow request detected: {name} took {response_time}ms")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when load test starts."""
    print("=" * 60)
    print("🚀 BlackCat AI CMS Load Test Starting")
    print("=" * 60)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when load test completes."""
    print("=" * 60)
    print("✅ Load Test Completed")
    print("=" * 60)
    stats = environment.stats
    print(f"Total Requests: {stats.total.num_requests}")
    print(f"Failed Requests: {stats.total.num_failures}")
    print(f"Average Response Time: {stats.total.avg_response_time:.2f}ms")
