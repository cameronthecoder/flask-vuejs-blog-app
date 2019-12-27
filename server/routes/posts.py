from flask import Blueprint, jsonify, request, g
from app import mysql, app
from json_utils import verify_parameters
from .auth import login_required
from .users import roles_required
from MySQLdb._exceptions import IntegrityError

posts_api = Blueprint('posts_api', __name__)

@posts_api.route('/')
def posts():
    cur = mysql.connection.cursor()
    query = """
    SELECT posts.id, posts.author_id, posts.title, posts.body, posts.draft, posts.created_at, posts.updated_at, posts.slug, users.username, users.role 
    FROM posts 
    INNER JOIN users 
    ON posts.author_id=users.id 
    WHERE draft = false;"""
    cur.execute(query)
    results = cur.fetchall()
    return jsonify({'posts': results})


@posts_api.route('/', methods=['POST'])
@verify_parameters(['title', 'body', 'slug'])
@login_required
@roles_required(['Administrator'])
def create_post():
    json = request.get_json()
    cur = mysql.connection.cursor()
    try:
        query = cur.execute('INSERT INTO posts (title, body, slug, author_id, draft) VALUES (%s, %s, %s, %s, %s)', (json['title'], json['body'], json['slug'], str(g.user['id']), json.get('draft', False)))
    except IntegrityError:
        cur.close()
        return jsonify({'error': 'That slug has been used before on another post. Please try another slug.'}), 400
    # Commit to DB
    mysql.connection.commit()

    object = cur.execute('SELECT * FROM posts WHERE id = %s', str(cur.lastrowid)) # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'post': result}), 201

@posts_api.route('/<int:id>/', methods=['PUT'])
@login_required
@roles_required(['Administrator'])
@verify_parameters(['title', 'body', 'slug'])
def edit_post(id):
    cur = mysql.connection.cursor()
    object = cur.execute(f'SELECT * FROM posts WHERE id = {id}')
    result = cur.fetchone()
    if not result:
        return jsonify({'error': 'That post does not exist.'}), 404
    # check if the user has permission to update this post
    if result['author_id'] != g.user['id']:
        return jsonify({'error': 'You do not have permission to update this post.'})
    json = request.get_json()
    try:
        query = cur.execute('UPDATE posts SET title = %s, body = %s, slug = %s WHERE id = %s', (json['title'], json['body'], json['slug'], str(id)))
        mysql.connection.commit()
    except IntegrityError:
        cur.close()
        return jsonify({'error': 'That slug has been used before on another post. Please try another slug.'}), 400
    cur.close()
    return jsonify({'success': 'The post has been successfully modified.'})


@posts_api.route('/<int:id>/', methods=['DELETE'])
@login_required
@roles_required(['Administrator'])
def delete_post(id):
    cur = mysql.connection.cursor()
    # Check if the post exists
    check = cur.execute('SELECT * FROM posts WHERE id = %s', (str(id)))
    result = cur.fetchone()
    if not result:
        return jsonify({'error': 'That post does not exist.'}), 404
    query = cur.execute('DELETE FROM posts WHERE id = %s', (str(id)))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': 'The post has been successfully deleted.'})

@posts_api.route('/filter/')
def filter():
    title = request.args.get('title', default='*', type = str)
    body = request.args.get('body', default='*', type = str)
    cur = mysql.connection.cursor()
    query = cur.execute('SELECT title, body FROM posts WHERE title LIKE %s OR body LIKE %s', ("%" + title + "%", "%" + body + "%"))
    result = cur.fetchall()
    return jsonify(result)

@posts_api.route('/<int:id>/', methods=['GET'])
def get_post(id):
    cur = mysql.connection.cursor()
    query = cur.execute('SELECT * FROM posts WHERE ID = %s', (str(id)))
    result = cur.fetchone()
    if result:
        return jsonify({'post': result})
    else:
        return jsonify({'error': 'That post does not exist.'}), 404
