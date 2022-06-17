"""
flaskr.utils.auth
~~~~~~~~~~~~~~~~~
Utilities for auth.
"""
import functools

from flask import g
from werkzeug.exceptions import abort


def login_required(view):
    """View decorator."""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            raise abort(401)

        return view(*args, **kwargs)

    return wrapped_view

