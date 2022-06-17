from pathlib import Path
from datetime import timedelta

from flask import Flask

from flaskr.config import settings
from flaskr.utils.encoder import JsonEncoder


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = JsonEncoder
    # Cannot use simple CORS to set cookies, because browsers changed Cookie setting to prevent CSRF
    # https://hacks.mozilla.org/2020/08/changes-to-samesite-cookie-behavior/
    app.config.from_mapping(
        SECRET_KEY="fbe8863a8b6687b6b59ce9f4284f657e366142fa88e969c800ae62d645b6705c",
        DATABASE=settings.DB_CONN,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=timedelta(days=settings.PERMANENT_SESSION_LIFETIME_DAYS),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # register the database commands
    from flaskr.utils import db
    if not Path(settings.DB_CONN).exists() or settings.DB_FORCE_RECREATE:
        db.init_db(app)
    db.init_app(app)
    # apply the blueprints to the app
    from flaskr.views import auth
    from flaskr.views import post

    app.register_blueprint(post.bp_index)
    app.register_blueprint(post.bp)
    app.register_blueprint(post.bp_comment)
    app.register_blueprint(auth.bp)

    @app.errorhandler(400)
    def args_wrong(e):
        return dict(error=str(e.description)), 400

    @app.errorhandler(403)
    def args_wrong(e):
        return dict(error=str(e.description)), 403

    return app


if __name__ == '__main__':
    _app = create_app()
    _app.run(debug=True)
