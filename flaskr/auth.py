from werkzeug.security import generate_password_hash

from flask import (
    Blueprint, request, flash, redirect, url_for, render_template
)

from .db import get_db_connection

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
                'SELECT id FROM user WHERE username = {}'.format(username)
        ).fetchone() is not None:
            error = "User {} is already registered".format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(pw)))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
