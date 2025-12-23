"""Tests for the signup endpoint."""

import pytest


def test_signup_for_activity_success(client, reset_activities):
    """Test successfully signing up for an activity."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert "newstudent@mergington.edu" in activities_data["Chess Club"]["participants"]


def test_signup_duplicate_email(client, reset_activities):
    """Test that duplicate signup returns an error."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "Already signed up" in data["detail"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signing up for a non-existent activity."""
    response = client.post(
        "/activities/Nonexistent%20Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_multiple_activities(client, reset_activities):
    """Test that a student can sign up for multiple activities."""
    email = "versatile@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        f"/activities/Chess%20Club/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        f"/activities/Programming%20Class/signup?email={email}"
    )
    assert response2.status_code == 200
    
    # Verify both signups
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data["Chess Club"]["participants"]
    assert email in activities_data["Programming Class"]["participants"]
