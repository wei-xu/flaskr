import sqlite3

from flask import current_app, g


def get_db_connection():
    if 'db' not in g:
        g.db_connection = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    return g.db_connection


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
