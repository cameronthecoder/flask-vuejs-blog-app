from flask import Blueprint, jsonify, request
from .auth import login_required
from app import mysql, app

posts_api = Blueprint('posts_api', __name__)

@posts_api.route('/', methods=['GET'])
def posts():
    cur = mysql.connection.cursor()
    query = cur.execute("SELECT * from posts")
    results = cur.fetchall()

    posts = []

    for post in results:
        posts.append({
            'id': post['id'],
            'title': post['title'],
            'body': post['body'],
            'slug': post['slug'],
            'created_at': post['created_at']
        })
    return jsonify({'posts': posts})


@posts_api.route('/', methods=['POST'])
@login_required
def create_post():
    json = request.get_json()
    if not 'title' in request.json or not 'body' in request.json or not 'slug' in request.json:
        return jsonify({'error': 'The title, body, and slug fields are required.'}), 422
    cur = mysql.connection.cursor()
    query = cur.execute('INSERT INTO posts (title, body, slug) VALUES (%s, %s, %s)', (json['title'], json['body'], json['slug']))
    # Commit to DB
    mysql.connection.commit()

    object = cur.execute(f'SELECT * FROM posts WHERE id = {cur.lastrowid}') # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'id': result['id'], 'title': result['title'], 'body': result['body'], 'slug': result['slug'], 'created_at': result['created_at']}), 201

@posts_api.route('/<int:id>/', methods=['PUT'])
def edit_post(id):
    cur = mysql.connection.cursor()
    object = cur.execute(f'SELECT * FROM posts WHERE id = {id}')
    result = cur.fetchone()
    if not result:
        return jsonify({'error': 'That post does not exist.'}), 404
    json = request.get_json()
    query = cur.execute(f'UPDATE posts SET title = "{json["title"]}", body = "{json["body"]}", slug = "{json["slug"]}" WHERE id = {id}')
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': 'The post has been successfully modified.'})


@posts_api.route('/<int:id>/', methods=['DELETE'])
@login_required
def delete_post(id):
    cur = mysql.connection.cursor()
    # Check if the post exists
    check = cur.execute(f'SELECT * FROM posts WHERE id = {id}')
    result = cur.fetchone()
    if not result:
        return jsonify({'error': 'That post does not exist.'}), 404
    query = cur.execute(f'DELETE FROM posts WHERE id = {id}')
    mysql.connection.commit()
    
    return jsonify({'success': 'The post has been successfully deleted.'})


@posts_api.route('/<int:id>/', methods=['GET'])
def get_post(id):
    cur = mysql.connection.cursor()
    query = cur.execute(f'SELECT * FROM posts WHERE ID = {id};')
    result = cur.fetchone()
    if result:
        return jsonify({'id': result['id'], 'title': result['title'], 'body': result['body'], 'slug': result['slug'], 'created_at': result['created_at']})
    else:
        return jsonify({'error': 'That post does not exist.'}), 404