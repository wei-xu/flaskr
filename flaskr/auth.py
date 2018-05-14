from flask import (
    Blueprint, request, flash, redirect, url_for, render_template, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db_connection

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # register this user
        # get information from request
        username = request.form['username']
        pw = request.form['password']

        error = None

        # have the database ready
        db = get_db_connection()

        if not username:
            error = "Unique user name is required to register"
        elif not pw:
            error = "Password is required to register"
        elif db.execute(
                'SELECT id FROM user WHERE username = ?',
                (username,)
        ).fetchone() is not None:
            error = "User {} is already registered".format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(pw)))
            db.commit()
            return redirect(url_for('.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # do login
        username = request.form['username']
        pw = request.form['password']

        error = None

        db = get_db_connection()

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if (not user) or (not check_password_hash(user['password'], pw)):
            error = 'Either username or password is incorrect'

        if error is None:
            # all form inputs are valid and hit a match in the database
            # the ultimate step is putting the user into session
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """Constantly check if a user a logged in and put the id into global"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db_connection().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view
