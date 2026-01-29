"""
Tests for the activities endpoints.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return all 9 activities
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Tennis Club" in data
    assert "Drama Club" in data
    assert "Visual Arts Studio" in data
    assert "Debate Team" in data
    assert "Robotics Club" in data


def test_get_activities_contains_required_fields(client):
    """Test that each activity has all required fields."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_get_activities_initial_participants(client):
    """Test that activities have the expected initial participants."""
    response = client.get("/activities")
    data = response.json()
    
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    assert "emma@mergington.edu" in data["Programming Class"]["participants"]
    assert "sophia@mergington.edu" in data["Programming Class"]["participants"]
