"""
Tests for the unregister/delete participant endpoint.
"""

import pytest


def test_unregister_participant_success(client):
    """Test successful removal of a participant."""
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "unregistered" in data["message"].lower()


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant."""
    # Remove participant
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test unregister fails for non-existent activity."""
    response = client.delete(
        "/activities/Fake Activity/participants",
        params={"email": "someone@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_nonexistent_participant(client):
    """Test unregister fails when participant is not in activity."""
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "notamember@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_maintains_other_participants(client):
    """Test that unregister only removes the specified participant."""
    # Get initial state
    response_before = client.get("/activities")
    participants_before = response_before.json()["Chess Club"]["participants"].copy()
    
    # Remove one participant
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify other participants remain
    response_after = client.get("/activities")
    participants_after = response_after.json()["Chess Club"]["participants"]
    
    assert "daniel@mergington.edu" in participants_after
    assert "michael@mergington.edu" not in participants_after
    assert len(participants_after) == len(participants_before) - 1


def test_unregister_then_signup_again(client):
    """Test that a participant can sign up again after being unregistered."""
    email = "michael@mergington.edu"
    
    # Remove participant
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": email}
    )
    
    # Sign up again
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify they're back in the list
    response = client.get("/activities")
    data = response.json()
    assert email in data["Chess Club"]["participants"]
