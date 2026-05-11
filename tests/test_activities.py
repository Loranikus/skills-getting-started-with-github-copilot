"""
Tests for the GET /activities endpoint.

Verifies that the activities endpoint returns the correct data structure,
contains all expected activities, and that each activity has required fields
with valid data types and values.
"""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    @pytest.mark.usefixtures("reset_activities")
    def test_returns_200_and_dict(self, client):
        """Test that GET /activities returns 200 status and dict response."""
        
        # Arrange
        # Using reset_activities and client fixtures
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.usefixtures("reset_activities")
    def test_contains_all_activities(self, client):
        """Test that GET /activities returns all 9 expected activities."""
        
        # Arrange
        expected_activities = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Debate Team",
            "Science Club"
        }
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert set(activities_data.keys()) == expected_activities
        assert len(activities_data) == 9

    @pytest.mark.usefixtures("reset_activities")
    @pytest.mark.parametrize("field", [
        "description",
        "schedule",
        "max_participants",
        "participants"
    ])
    def test_each_activity_has_required_fields(self, client, field):
        """Test that all activities contain all required fields."""
        
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert field in activity_info, f"{activity_name} missing {field}"
            assert set(activity_info.keys()) == required_fields

    @pytest.mark.usefixtures("reset_activities")
    def test_participants_is_list(self, client):
        """Test that participants field contains a list for all activities."""
        
        # Arrange
        # Using reset_activities and client fixtures
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["participants"], list), \
                f"{activity_name} participants should be a list"
            for participant in activity_info["participants"]:
                assert isinstance(participant, str), \
                    f"Participant in {activity_name} should be a string"

    @pytest.mark.usefixtures("reset_activities")
    def test_description_is_non_empty_string(self, client):
        """Test that all activities have non-empty description strings."""
        
        # Arrange
        # Using reset_activities and client fixtures
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["description"], str)
            assert len(activity_info["description"]) > 0, \
                f"{activity_name} has empty description"

    @pytest.mark.usefixtures("reset_activities")
    def test_schedule_is_non_empty_string(self, client):
        """Test that all activities have non-empty schedule strings."""
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["schedule"], str)
            assert len(activity_info["schedule"]) > 0, \
                f"{activity_name} has empty schedule"

    @pytest.mark.usefixtures("reset_activities")
    def test_max_participants_is_positive_integer(self, client):
        """Test that max_participants is a positive integer for all activities."""
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"
            assert activity_info["max_participants"] > 0, \
                f"{activity_name} max_participants should be positive"

    @pytest.mark.usefixtures("reset_activities")
    def test_participants_count_within_max(self, client):
        """Test that participant count does not exceed max_participants."""
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            participants_count = len(activity_info["participants"])
            max_participants = activity_info["max_participants"]
            assert participants_count <= max_participants, \
                f"{activity_name} has too many participants"
