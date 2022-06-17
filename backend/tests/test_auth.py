import pytest
from flask import session

from flaskr.utils.db import get_db


def test_register(client, app):
    assert client.get("/api/auth/register").status_code == 405

    response = client.post("/api/auth/register", data={"username": "a", "password": "a"})
    assert response.status_code == 400

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM user WHERE username = 'aBCs3'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "email", "message"),
    (
        ("", "", "", b"Username is required."),
        ("a", "", "", b"Password is required."),
        ("a", "b", "", b"E-mail is required."),
        ("a", "b", "a", b"Invalid E-mail address."),
        ("a", "b", "a@abc.com", b"Invalid username."),
        ("a22lBs", "b", "a@abc.com", b"Invalid password."),
        ("aBCs3", "ABCISLisli229*90", "a@b.com", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        "/api/auth/register", data={"username": username, "password": password, "email": email}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get("/api/auth/login").status_code == 401

    response = auth.login()
    assert response.status_code == 200

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["token"] == response.text


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("asdfs2L", "test", b"Invalid username, email or password"), ("test", "aLLLk2lk*@slk", b"Invalid username, email or password")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    with client:
        auth.login()
        assert "token" in session
        auth.logout()
        assert "token" not in session
