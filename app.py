import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# Create a link Database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a single page Post
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'

@app.route('/')
def index():
    conn = get_db_connection()
    table_posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=table_posts )

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

# Create a Post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES(?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# Edit Post
@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post = get_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is not required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         'WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close
            return redirect(url_for('index'))
    
    return render_template('edit.html', post=post)
        
# Delete Post
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(
        debug=True, passthrough_errors=True, use_debugger=False, use_reloader=False, host="0.0.0.0", port=os.environ['PORT']
    )