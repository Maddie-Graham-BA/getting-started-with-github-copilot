"""
Tests for the signup endpoint.
"""

import pytest


def test_signup_for_activity_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newemail@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newemail@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_updates_participant_list(client):
    """Test that signup adds the participant to the activity."""
    # Sign up new participant
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity(client):
    """Test signup fails for non-existent activity."""
    response = client.post(
        "/activities/Non Existent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_student(client):
    """Test that duplicate signup is rejected."""
    # Try to sign up a student who is already registered
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}  # Already signed up
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_activities_same_student(client):
    """Test that a student can sign up for multiple activities."""
    student_email = "versatile@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": student_email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": student_email}
    )
    assert response2.status_code == 200
    
    # Verify both signups
    response = client.get("/activities")
    data = response.json()
    assert student_email in data["Chess Club"]["participants"]
    assert student_email in data["Programming Class"]["participants"]


def test_signup_maintains_other_participants(client):
    """Test that signup doesn't affect other participants."""
    # Get initial state
    response_before = client.get("/activities")
    chess_before = response_before.json()["Chess Club"]["participants"].copy()
    
    # Sign up new participant for a different activity
    client.post(
        "/activities/Programming Class/signup",
        params={"email": "newperson@mergington.edu"}
    )
    
    # Verify Chess Club participants haven't changed
    response_after = client.get("/activities")
    chess_after = response_after.json()["Chess Club"]["participants"]
    assert chess_before == chess_after
