from flask import Blueprint, request, jsonify, request
from functools import wraps
from app import app, mysql
from datetime import datetime, timedelta
import jwt, bcrypt
auth_api = Blueprint('auth_api', __name__)

# Login Required Middleware
def login_required(f):
    "Makes sure the request contains a Bearer token to authenticate the user before the request is fully processed."
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
                except jwt.DecodeError:
                    return jsonify({'error': 'Token expired or invalid.'}), 401
            else:
                return jsonify({'error': 'Token expired or invalid.'}), 401
        else:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_api.route('/api/users/', methods=['POST'])
@login_required
def create_user():
    json = request.get_json()
    if not 'username' in request.json or not 'password' in request.json:
        return jsonify({'error': 'The username and password fields are required.'}), 422
    cur = mysql.connection.cursor()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(json['password'].encode('utf-8'), salt)
    query = cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (json['username'], hashed))
    mysql.connection.commit()

    object = cur.execute(f'SELECT * FROM users WHERE id = {cur.lastrowid}') # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'id': result['id'], 'username': result['username'], 'active': result['active'], 'password': result['password']})

@auth_api.route('/auth/login/', methods=['POST'])
def login():
    json = request.get_json()
    if not 'username' in request.json or not 'password' in request.json:
        return jsonify({'error': 'The username and password fields are required.'}), 422
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