"""Role-based access control decorators."""

from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    """Decorator: restrict route to admin role only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('يرجى تسجيل الدخول أولا', 'warning')
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def editor_required(f):
    """Decorator: restrict route to admin or editor roles."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('يرجى تسجيل الدخول أولا', 'warning')
            return redirect(url_for('auth.login'))
        if current_user.role not in ('admin', 'editor'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def viewer_required(f):
    """Decorator: restrict route to authenticated users (all roles)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('يرجى تسجيل الدخول أولا', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
