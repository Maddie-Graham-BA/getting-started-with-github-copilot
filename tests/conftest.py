"""
Pytest configuration and fixtures for the Mergington High School API tests.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add src directory to path so we can import app
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for all skill levels",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn and play tennis with coaching",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 12,
            "participants": ["alex@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Visual Arts Studio": {
            "description": "Explore painting, drawing, sculpture, and mixed media",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["sophia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in debate competitions and develop argumentation skills",
            "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["marcus@mergington.edu", "rachel@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for competitions",
            "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["kevin@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset again after test
    activities.clear()
    activities.update(original_activities)
