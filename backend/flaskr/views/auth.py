import functools
from uuid import uuid1
from typing import Tuple
from datetime import datetime, timedelta

import schema
from flask import g
from flask import request
from flask import session
from flask import Blueprint, abort
from flask.views import MethodView
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr import settings
from flaskr.utils.db import get_db
from flaskr.utils.check_input import check_input, email_pattern, username_pattern, password_pattern

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.before_app_request
def load_logged_in_user():
    """If a user token is stored in the session, load the user object from
    the database into ``g.user``."""
    token = session.get("token")

    if token is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE token = :token and token_expired_at >= :now", {"token": token, "now": datetime.now()}).fetchone()


@bp.route("/logout", methods=("POST", "GET"))
def logout():
    """Clear the current session, including the stored user token."""
    session.clear()
    return dict(ok="ok")


@bp.route("/register", methods=("POST", ))
def register():
    """Register a new user.

    Validates that the username or email is not already taken. Hashes the
    password for security.
    :param [form] username:
    :param [form] email:
    :param [form] password:
    :raise 400: Username is required.
    :raise 400: Password is required.
    :raise 400: E-mail is required.
    :raise 400: Invalid E-mail address.
    :raise 400: Invalid username.
    :raise 400: Invalid password.
    :return json 201: {"username": <username>}
    """
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get('email')

    if not username:
        abort(400, description="Username is required.")
    elif not password:
        abort(400, description="Password is required.")
    elif not email:
        abort(400, description="E-mail is required.")
    if not check_input(email, pattern=email_pattern):
        abort(400, description="Invalid E-mail address.")
    if not check_input(username, pattern=username_pattern):
        abort(400, description="Invalid username.")
    if not check_input(password, pattern=password_pattern):
        abort(400, description="Invalid password.")
    token = str(uuid1())

    db = get_db()
    try:
        with db:
            db.execute(
                "INSERT INTO user (username, password, email, token, token_expired_at) VALUES (?, ?, ?, ?, ?)",
                (username, generate_password_hash(password), email, token, datetime.now() + timedelta(days=settings.PERMANENT_SESSION_LIFETIME_DAYS)),
            )
    except db.IntegrityError:
        # The username was already taken, which caused the
        # commit to fail. Show a validation error.
        abort(400, f"User {username} or Email {email} is already registered.")
    else:
        # Success, go to the login page.
        # return redirect(url_for("auth.login"))
        session.clear()
        session["token"] = token
        return dict(username=username), 201


class Login(MethodView):
    def get(self):
        """
        Get login status.
        :raise 401: if not login
        :return text 200: username
        """
        token = session.get("token")

        if token is None:
            g.user = None
            return '', 401
        else:
            g.user = get_db().execute("SELECT * FROM user WHERE token = :token and token_expired_at >= :now",
                                      {"token": token, "now": datetime.now()}).fetchone()
            if not g.user:
                session.clear()
                return '', 401
            return f"{g.user['username']}({g.user['email']})"

    def post_schema(self, form_dict: dict) -> Tuple[str, str, bool]:
        try:
            data = schema.Schema({
                "username": schema.Or(  # support both username and email
                    functools.partial(check_input, pattern=username_pattern),
                    functools.partial(check_input, pattern=email_pattern)
                ),
                "password": functools.partial(check_input, pattern=password_pattern),
                schema.Optional("rememberme", default=False): schema.Use(bool)
            }).validate(form_dict)
        except schema.SchemaError as e:
            print(e)
            raise abort(400, description="Invalid username, email or password.")
        else:
            return data["username"], data["password"], data['rememberme']

    def post(self):
        """
        Log in a registered user by adding the user id to the session.
        :param form username: username or email to login.
        :param form password:
        :param form rememberme: bool, permanent cookie and session
        :return text 200: token
        :raise 403 Incorrect username:
        :raise 403 Incorrect password:
        :raise 400 Invalid username, email or password:
        """
        username, password, rememberme = self.post_schema(dict(request.form))

        db = get_db()
        user = db.execute(
            "SELECT id, password FROM user WHERE username = ? or email = ?",
            (username, username, )
        ).fetchone()

        if user is None:
            raise abort(403, "Incorrect username.")
        elif not check_password_hash(user["password"], password):   # `hmac.compare_digest` to prevent timing analysis
            raise abort(403, "Incorrect password.")
        else:
            token = str(uuid1())
            db.execute(
                f"UPDATE user SET token = ? , token_expired_at = ? WHERE id = ?",
                (token, datetime.now() + timedelta(days=settings.PERMANENT_SESSION_LIFETIME_DAYS), user['id'])
            )
            db.commit()

            # store the user id in a new session and return to the index
            session.clear()
            session["token"] = token
            if rememberme:
                session.permanent = True
            return token


bp.add_url_rule('/login', view_func=Login.as_view('login'))

