import pytest
from flask import session

from flaskr.utils.db import get_db


def test_post(client, auth):
    response = client.get("/api", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize("path", ("/api/post", "/api/post/1/comment"))
def test_login_required(client, path):
    response = client.post(path, follow_redirects=True)
    assert response.status_code == 401


@pytest.mark.parametrize("path", ("/api/post/2/comment", ))
def test_exists_required(client, auth, path):
    response = auth.login()
    assert response.status_code == 200
    assert client.post(path).status_code == 400


def test_create(client, auth, app):
    auth.login()
    response = client.post("/api/post", data={"title": "created", "body": "testtest"}, follow_redirects=True)
    assert response.status_code == 201

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 2


def test_create_validate(client, auth):
    auth.login()
    response = client.post("/api/post", data={"title": "created", "body": ""}, follow_redirects=True)
    assert response.status_code == 400
    assert b"Wrong args." in response.data
