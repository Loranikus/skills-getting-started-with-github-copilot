"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.

Verifies that participants can unregister from activities, error cases are
handled correctly, and participant lists are updated appropriately.
"""

import pytest


class TestUnregister:
    """Test suite for the DELETE /unregister endpoint."""

    @pytest.mark.usefixtures("reset_activities")
    def test_successful_unregister(self, client):
        """Test successful unregistration removes participant and returns 200."""
        
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]

    @pytest.mark.usefixtures("reset_activities")
    def test_unregister_removes_from_activities_list(self, client):
        """Test that unregistered participant is removed from activities list."""
        
        # Arrange
        email = "emma@mergington.edu"
        activity = "Programming Class"
        initial_response = client.get("/activities")
        assert email in initial_response.json()[activity]["participants"]
        initial_count = len(initial_response.json()[activity]["participants"])
        
        # Act
        client.delete(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity]["participants"]
        assert email not in final_participants
        assert len(final_participants) == initial_count - 1

    @pytest.mark.usefixtures("reset_activities")
    def test_unregister_not_registered_returns_400(self, client):
        """Test that unregistering non-registered participant returns 400."""
        
        # Arrange
        email = "notregistered@mergington.edu"
        activity = "Tennis Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    @pytest.mark.usefixtures("reset_activities")
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test that unregistration from non-existent activity returns 404."""
        
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    @pytest.mark.usefixtures("reset_activities")
    def test_signup_then_unregister_workflow(self, client):
        """Test full workflow: signup to activity then unregister."""
        
        # Arrange: Setup
        email = "workflow@mergington.edu"
        activity = "Art Studio"
        client.post(f"/activities/{activity}/signup?email={email}")
        verify_response = client.get("/activities")
        assert email in verify_response.json()[activity]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        final_response = client.get("/activities")
        assert email not in final_response.json()[activity]["participants"]
