from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user, AnonymousUserMixin


def team_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'team':
            return redirect(url_for('core.main'))
        else:
            return f(*args, **kwargs)

    return decorated_function


def candidate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'candidate':
            return redirect(url_for('core.main'))
        else:
            return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'admin':
            return redirect(url_for('core.main'))
        else:
            return f(*args, **kwargs)

    return decorated_function


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('core.login'))
        else:
            return f(*args, **kwargs)

    return decorated_function
