"""Tests for the activities endpoints."""

import pytest


def test_get_activities(client):
    """Test getting all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    
    # Verify activity structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_get_activities_contains_expected_fields(client):
    """Test that activities have all required fields."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details["description"], str)
        assert isinstance(activity_details["schedule"], str)
        assert isinstance(activity_details["max_participants"], int)
        assert isinstance(activity_details["participants"], list)


def test_chess_club_has_initial_participants(client):
    """Test that Chess Club has initial participants."""
    response = client.get("/activities")
    data = response.json()
    chess_club = data["Chess Club"]
    
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
