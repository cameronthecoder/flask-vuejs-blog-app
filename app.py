from flask import Flask, request, render_template, redirect, url_for, jsonify
from functools import wraps
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import bcrypt, jwt, os

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']

# Login Required Middleware
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            if 'Bearer' in request.headers.get('Authorization'):
                token = request.headers.get('Authorization').split(' ')[1] # The format would be Bearer <token>
                try:
                    jwt.decode(token, app.config['SECRET_KEY'], issuer='blogapp', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    return jsonify({'error': 'Token expired or invalid.'}), 401
                except jwt.InvalidIssuerError:
                    return jsonify({'error': 'Token expired or invalid.'}), 401
            else:
                return jsonify({'error': 'Token expired or invalid.'}), 401
        else:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/users/create/', methods=['POST'])
def create_user():
    json = request.get_json()
    cur = mysql.connection.cursor()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(json['password'].encode('utf-8'), salt)
    query = cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (json['username'], hashed))
    mysql.connection.commit()

    object = cur.execute(f'SELECT * FROM users WHERE id = {cur.lastrowid}') # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'id': result['id'], 'title': result['username'], 'active': result['active'], 'password': result['password']})

@app.route('/auth/login/', methods=['POST'])
def login():
    json = request.get_json()
    cur = mysql.connection.cursor()
    query = cur.execute('SELECT * FROM users WHERE username = %s', [json['username']])
    result = cur.fetchone()
    if query:
        if not result['active']:
            return jsonify({'error': 'That user is not active.'}), 401
        elif not bcrypt.checkpw(json['password'].encode('utf-8'), result['password'].encode('utf-8')):
            return jsonify({'error': 'The username or password is incorrect.'}), 401
        else:
            encoded_jwt = jwt.encode({'id': result['id'], 'username': json['username'], 'exp': datetime.utcnow() + timedelta(days=1), 'iss': 'blogapp'}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': encoded_jwt})


@app.route('/api/posts/')
def users():
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


@app.route('/api/posts/create/', methods=['POST'])
@login_required
def create_post():
    json = request.get_json()
    cur = mysql.connection.cursor()
    query = cur.execute('INSERT INTO posts (title, body, slug) VALUES (%s, %s, %s)', (json['title'], json['body'], json['slug']))
    # Commit to DB
    mysql.connection.commit()

    object = cur.execute(f'SELECT * FROM posts WHERE id = {cur.lastrowid}') # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'id': result['id'], 'title': result['title'], 'body': result['body'], 'slug': result['slug'], 'created_at': result['created_at']})


@app.route('/api/posts/<int:id>/delete/', methods=['DELETE'])
@login_required
def delete_post(id):
    json = request.get_json()
    cur = mysql.connection.cursor()
    query = cur.execute(f'DELETE FROM posts WHERE id = {id}')
    mysql.connection.commit()
    return jsonify({'success': 'The post has been successfully deleted.'})


@app.route('/post/<int:id>/')
def get_post(id):
    cur = mysql.connection.cursor()
    query = cur.execute(f'SELECT * FROM posts WHERE ID = {id};')
    result = cur.fetchone()
    if result:
        return jsonify({'id': result['id'], 'title': result['title'], 'body': result['body'], 'slug': result['slug'], 'created_at': result['created_at']})
    else:
        return jsonify({'error': 'That post does not exist.'}), 500

if __name__ == "__main__":
    app.run(debug=True)