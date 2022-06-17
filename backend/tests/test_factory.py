import tempfile

from flaskr import create_app


def test_config():
    """Test create_app without passing test config."""
    db_fd, db_path = tempfile.mkstemp()
    assert not create_app({"TESTING": False, "DATABASE": db_path}).testing
    assert create_app({"TESTING": True, "DATABASE": db_path}).testing
