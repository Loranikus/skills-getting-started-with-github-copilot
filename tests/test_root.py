"""
Tests for the GET / root endpoint.

Verifies that the root endpoint correctly redirects to the static 
index.html file with the appropriate HTTP status code.
"""

import pytest


class TestRootEndpoint:
    """Test suite for the GET / endpoint."""

    def test_root_redirects_to_static_index_html(self, client):
        """Test that GET / redirects to /static/index.html with status 307."""
        
        expected_status_code = 307
        expected_location = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == expected_status_code
        assert "location" in response.headers
        assert response.headers["location"] == expected_location
