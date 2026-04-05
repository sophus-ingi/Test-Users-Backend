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
    
    # Set port: 3306 for Docker/CI, 3307 for local localhost
    if 'DB_PORT' not in os.environ:
        db_host = os.environ.get('DB_HOST', 'db')
        os.environ['DB_PORT'] = '3307' if db_host == 'localhost' else '3306'
    
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
