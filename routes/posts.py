from flask import Blueprint, jsonify, request, g
from .auth import login_required
from app import mysql, app

posts_api = Blueprint('posts_api', __name__)

@posts_api.route('/', methods=['GET'])
def posts():
    cur = mysql.connection.cursor()
    query = cur.execute("SELECT * from posts WHERE draft = false")
    results = cur.fetchall()
    return jsonify({'posts': results})


@posts_api.route('/', methods=['POST'])
@login_required
def create_post():
    json = request.get_json()
    print(g.user['id'])
    if not 'title' in json or not 'body' in json or not 'slug' in json:
        return jsonify({'error': 'The title, body, and slug fields are required.'}), 422
    cur = mysql.connection.cursor()
    query = cur.execute('INSERT INTO posts (title, body, slug, author_id, draft) VALUES (%s, %s, %s, %s, %s)', (json['title'], json['body'], json['slug'], g.user['id'], json.get('draft', False)))
    # Commit to DB
    mysql.connection.commit()

    object = cur.execute('SELECT * FROM posts WHERE id = %s', (cur.lastrowid)) # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'post': result}), 201

@posts_api.route('/<int:id>/', methods=['PUT'])
@login_required
def edit_post(id):
    cur = mysql.connection.cursor()
    object = cur.execute(f'SELECT * FROM posts WHERE id = {id}')
    result = cur.fetchone()
    if not result:
        return jsonify({'error': 'That post does not exist.'}), 404
    json = request.get_json()
    query = cur.execute('UPDATE posts SET title = %s, body = %s, slug = %s WHERE id = %s', (json['title'], json['body'], json['slug'], str(id)))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': 'The post has been successfully modified.'})


@posts_api.route('/<int:id>/', methods=['DELETE'])
@login_required
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


@posts_api.route('/<int:id>/', methods=['GET'])
def get_post(id):
    cur = mysql.connection.cursor()
    query = cur.execute('SELECT * FROM posts WHERE ID = %s', (str(id)))
    result = cur.fetchone()
    if result:
        return jsonify({'post': result})
    else:
        return jsonify({'error': 'That post does not exist.'}), 404