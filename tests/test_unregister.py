"""Tests for the unregister endpoint."""

import pytest


def test_unregister_success(client, reset_activities):
    """Test successfully unregistering from an activity."""
    email = "michael@mergington.edu"
    
    # Verify participant is in the activity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data["Chess Club"]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={email}",
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    
    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data["Chess Club"]["participants"]


def test_unregister_not_registered(client, reset_activities):
    """Test unregistering a participant who isn't registered."""
    email = "notregistered@mergington.edu"
    
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={email}",
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "Not registered" in data["detail"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregistering from a non-existent activity."""
    response = client.delete(
        "/activities/Nonexistent%20Club/unregister?email=someone@mergington.edu",
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_then_signup_again(client, reset_activities):
    """Test that a participant can sign up again after unregistering."""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Unregister
    response1 = client.delete(
        f"/activities/{activity.replace(' ', '%20')}/unregister?email={email}",
    )
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post(
        f"/activities/{activity.replace(' ', '%20')}/signup?email={email}"
    )
    assert response2.status_code == 200
    
    # Verify they're registered again
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity]["participants"]
