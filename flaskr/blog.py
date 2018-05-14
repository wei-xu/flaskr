from flask import Blueprint, render_template, request, flash, g, redirect, url_for, abort

from db import get_db_connection

from auth import login_required

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db_connection()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p JOIN user u on p.author_id = u.id '
        'ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


def get_post(id, check_author=True):
    post = get_db_connection().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db_connection()
            db.execute(
                'INSERT INTO posts (title, body, author_id) '
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    else:
        return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db_connection()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog.update.html', post=post)


@bp.route('/<int:id>/delete', methods=['POST', ])
@login_required
def delete(id):
    # validate existance
    get_post(id)
    db = get_db_connection()
    db.execute(
        'DELETE FROM posts WHERE id = ?',
        (id, )
    )
    db.commit()
    return redirect(url_for('blog.index'))


