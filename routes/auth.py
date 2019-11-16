from flask import Blueprint, request, jsonify, request, g, abort
from functools import wraps
from app import app, mysql
from json_utils import verify_parameters
from datetime import datetime, timedelta
import jwt, bcrypt, MySQLdb

auth_api = Blueprint('auth_api', __name__)

def verify_token(token):
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], issuer='blogapp', algorithms=['HS256'])
    except:
        return False
    return decoded

# Login Required Middleware
def login_required(f):
    "This function will make sure the request contains a Bearer token to authenticate the user before the request is fully processed."
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the headers contain a valid Authorization header
        if 'Authorization' in request.headers:
            if 'Bearer' in request.headers.get('Authorization'):
                token = request.headers.get('Authorization').split()[1] # The format would be Bearer <token>
                # Decode the token and throw an error if the token is invalid
                # Query the database to make sure the user exists and is has an active account
                decoded_token = verify_token(token)
                if not decoded_token(token): return jsonify({'error': 'Invalid token'}), 401
                cur = mysql.connection.cursor()
                query = cur.execute(f'SELECT * FROM users WHERE id = {decoded_token["id"]}')
                result = cur.fetchone()
                # Throws an error if the user doesn't exist or isn't active
                if not result:
                    return jsonify({'error': 'That user does not exist.'}), 401
                if not result['active']:
                    return jsonify({'error': 'User account is not active.'}), 401
                g.user = result
            else:
                return jsonify({'error': 'Token expired or invalid.'}), 401
        else:
            return jsonify({'error': 'Missing JWT token.'}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_api.route('/refresh_token/', methods=['POST'])
def refresh_token():
    token = request.headers.get('Authorization').split()[1]
    decoded_token = verify_token(token)
    if not decoded_token(token): return jsonify({'error': 'Invalid token'}), 401
    cur = mysql.connection.cursor() 
    query = cur.execute(f'SELECT * FROM users WHERE id = {decoded_token["id"]}')
    result = cur.fetchone()
    # Throws an error if the user doesn't exist or isn't active
    if not result:
        return jsonify({'error': 'That user does not exist.'}), 401
    if not result['active']:
        return jsonify({'error': 'User account is not active.'}), 401

    access_token = jwt.encode({'id': result['id'], 'username': result['username'], 'exp': datetime.utcnow() + timedelta(seconds=180), 'iss': 'blogapp'}, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'access_token': access_token})
    
@auth_api.route('/login/', methods=['POST'])
@verify_parameters(['username', 'password'])
def login():
    # Get the JSON from the request
    json = request.get_json()
    # Check if the JSON contains the keys needed to login
    #if not 'username' in json or not 'password' in json:
    #    return jsonify({'error': 'The username and password fields are required.'}), 422
    cur = mysql.connection.cursor()
    query = cur.execute('SELECT * FROM users WHERE username = %s', [json['username']])
    result = cur.fetchone()
    # Check's if the user exists
    if result:
        # Throw an error if the user is not active
        if not result['active']:
            return jsonify({'error': 'That user is not active.'}), 401
        # Throw an error if the password is not correct.
        elif not bcrypt.checkpw(json['password'].encode('utf-8'), result['password'].encode('utf-8')):
            return jsonify({'error': 'The username or password is incorrect.'}), 401
        # If everything is okay, encode a JWT token with the user's ID and username in the body and set the expiration date aswell as the issuer
        else:
            access_token = jwt.encode({'id': result['id'], 'username': json['username'], 'exp': datetime.utcnow() + timedelta(seconds=180), 'iss': 'blogapp'}, app.config['SECRET_KEY'], algorithm='HS256')
            refresh_token = jwt.encode({'exp': datetime.utcnow() + timedelta(days=14), 'iss': 'blogapp'}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'refresh_token': refresh_token, 'access_token': access_token})
    else:
        return jsonify({'error': 'That user does not exist.'}), 401
