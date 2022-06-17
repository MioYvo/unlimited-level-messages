import pytest

from flaskr.utils.db import get_db


def test_comment(client, auth):
    response = client.get("/api/post/1/comment", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize("path", ("/api/comment/1/comment", ))
def test_login_required(client, path):
    response = client.post(path, follow_redirects=True)
    assert response.status_code == 401


@pytest.mark.parametrize("path", ("/api/comment/2/comment", ))
def test_exists_required(client, auth, path):
    response = auth.login()
    assert response.status_code == 200
    assert client.post(path).status_code == 400


def test_create(client, auth, app):
    auth.login()
    response = client.post("/api/post/1/comment", data={"body": "commenttest"}, follow_redirects=True)
    assert response.status_code == 201

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM comment WHERE post_id=1").fetchone()[0]
        assert count == 1

    response = client.post("/api/comment/1/comment", data={"body": "commenttest1"}, follow_redirects=True)
    assert response.status_code == 201

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM comment WHERE post_id=1").fetchone()[0]
        assert count == 2

    response = client.get("/api/post/1", follow_redirects=True)
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert len(response.json['comments']) == 1
    assert response.json['comments'][0]['id'] == 1
    assert response.json['comments'][0]['body'] == 'commenttest'
    assert len(response.json['comments'][0]['children']) == 1
    assert response.json['comments'][0]['children'][0]['id'] == 2
    assert response.json['comments'][0]['children'][0]['body'] == 'commenttest1'
    assert 'children' in response.json['comments'][0]['children'][0]

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM comment WHERE post_id=1").fetchone()[0]
        assert count == 2


def test_create_validate(client, auth):
    auth.login()
    response = client.post("/api/post/1/comment", data={"body": ""}, follow_redirects=True)
    assert response.status_code == 400
    assert b"Wrong args." in response.data
