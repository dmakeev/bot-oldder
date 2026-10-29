"""Common fixtures for PROсрочка tests."""
import pytest
import os

# Set environment variables for tests
os.environ["BOT_TOKEN"] = "test_token"
os.environ["ADMIN_USER_ID"] = "123456"
os.environ["DB_PATH"] = "/tmp/test_prosrochka.db"
