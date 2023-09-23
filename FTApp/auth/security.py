from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def team_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'team':
            return redirect(url_for('main_router.main'))
        else:
            return f(*args, **kwargs)

    return decorated_function


def candidate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'candidate':
            return redirect(url_for('main_router.main'))
        else:
            return f(*args, **kwargs)

    return decorated_function


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        else:
            return f(*args, **kwargs)

    return decorated_function
