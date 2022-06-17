import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.utils.db import get_db
from flaskr.utils.db import init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db(app)
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="aBCs3", password="ABCISLisli229*90"):
        return self._client.post(
            "/api/auth/login", data={"username": username, "password": password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get("/api/auth/logout", follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)
