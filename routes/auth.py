from flask import Blueprint, request, jsonify, request, g, abort
from functools import wraps
from app import app, mysql
from json_utils import verify_parameters
from datetime import datetime, timedelta
import jwt, bcrypt, MySQLdb

auth_api = Blueprint('auth_api', __name__)

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
                try:
                    decoded = jwt.decode(token, app.config['SECRET_KEY'], issuer='blogapp', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    return jsonify({'error': 'Token expired.'}), 401
                except jwt.InvalidIssuerError:
                    return jsonify({'error': 'Token contains an invalid issuer.'}), 401
                except jwt.DecodeError:
                    return jsonify({'error': 'Token invalid.'}), 401
                cur = mysql.connection.cursor()
                query = cur.execute(f'SELECT * FROM users WHERE id = {decoded["id"]}')
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
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], issuer='blogapp', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired.'}), 401
    except jwt.InvalidIssuerError:
        return jsonify({'error': 'Token contains an invalid issuer.'}), 401
    except jwt.DecodeError:
        return jsonify({'error': 'Token invalid.'}), 401
    cur = mysql.connection.cursor() 
    query = cur.execute(f'SELECT * FROM users WHERE id = {decoded["id"]}')
    result = cur.fetchone()
    # Throws an error if the user doesn't exist or isn't active
    if not result:
        return jsonify({'error': 'That user does not exist.'}), 401
    if not result['active']:
        return jsonify({'error': 'User account is not active.'}), 401

    access_token = jwt.encode({'id': result['id'], 'username': result['username'], 'exp': datetime.utcnow() + timedelta(seconds=180), 'iss': 'blogapp'}, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'access_token': access_token.decode('utf-8')})
    
@auth_api.route('/login/', methods=['POST'])
@verify_parameters(['username', 'password'])
def login():
    # Get the JSON from the request
    json = request.get_json()
    # Check if the JSON contains the keys needed to login
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
            access_token = jwt.encode(
                {'id': result['id'], 'username': json['username'], 
                'exp': datetime.utcnow() + timedelta(seconds=180), 
                'iss': 'blogapp'}, app.config['SECRET_KEY'], 
                algorithm='HS256')
            refresh_token = jwt.encode(
                {'exp': datetime.utcnow() + timedelta(days=14), 'iss': 'blogapp'}, 
                app.config['SECRET_KEY'], algorithm='HS256')
            # Convert JWT's to strings :)
            return jsonify({'refresh_token': refresh_token.decode('utf-8'), 'access_token': access_token.decode('utf-8')})
            
    else:
        return jsonify({'error': 'That user does not exist.'}), 401
