"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Verifies that students can sign up for activities, duplicates are prevented,
error cases are handled correctly, and participant lists are updated.
"""

import pytest


class TestSignup:
    """Test suite for the POST /signup endpoint."""

    @pytest.mark.usefixtures("reset_activities")
    def test_successful_signup(self, client):
        """Test successful signup adds participant to activity and returns 200."""
        
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]
        assert activity in response.json()["message"]

    @pytest.mark.usefixtures("reset_activities")
    def test_signup_appears_in_activities_list(self, client):
        """Test that newly signed up participant appears in activities list."""
        
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Gym Class"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity]["participants"])
        
        # Act
        client.post(f"/activities/{activity}/signup?email={email}")
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity]["participants"])
        
        # Assert
        assert final_count == initial_count + 1
        assert email in final_response.json()[activity]["participants"]

    @pytest.mark.usefixtures("reset_activities")
    def test_duplicate_signup_returns_400(self, client):
        """Test that repeated signup with same email returns 400 error."""
        
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Act - try to signup someone already in Chess Club
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    @pytest.mark.usefixtures("reset_activities")
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signup to non-existent activity returns 404."""
        
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    @pytest.mark.usefixtures("reset_activities")
    @pytest.mark.parametrize("activity", [
        "Programming Class",
        "Art Studio",
        "Science Club",
        "Music Band"
    ])
    def test_signup_multiple_activities(self, client, activity):
        """Test successful signup for various activities."""
        
        # Arrange
        email = f"student-{activity.replace(' ', '-')}@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]
