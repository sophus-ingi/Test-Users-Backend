"""
Pytest configuration and fixtures.

Sets up test environment, database, and fixtures for all tests.
"""

import os
import pytest


def pytest_configure(config):
    """Configure pytest and set up test environment."""
    # Set up test database environment variables
    os.environ['DB_HOST'] = os.getenv('DB_HOST', 'db')
    os.environ['DB_NAME'] = os.getenv('DB_NAME', 'addresses')
    os.environ['DB_USER'] = os.getenv('DB_USER', 'root')
    os.environ['DB_PASSWORD'] = os.getenv('DB_PASSWORD', '')
    os.environ['FLASK_ENV'] = 'testing'


@pytest.fixture(scope="session")
def test_env():
    """Provide test environment variables."""
    return {
        'DB_HOST': os.getenv('DB_HOST', 'db'),
        'DB_NAME': os.getenv('DB_NAME', 'addresses'),
        'DB_USER': os.getenv('DB_USER', 'root'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD', ''),
    }
