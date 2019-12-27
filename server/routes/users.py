from flask import Blueprint, request, jsonify, request, g, abort
from app import app, mysql
from .auth import login_required
from json_utils import verify_parameters
from getpass import getpass
from functools import wraps
from MySQLdb._exceptions import IntegrityError
import click, bcrypt

users_api = Blueprint('users_api', __name__, cli_group=None)

def roles_required(roles: dict):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                print(g.user)
            except:
                # The login required decorator is not added to the route.
                return jsonify({'error': 'The user is not set.'}), 500
            if not g.user['role'] in roles:
                if request.method == "POST":
                    return jsonify({'error': 'You do not have permission to create a new resource.'}), 403
                elif request.method == "GET":
                    return jsonify({'error': 'You do not have permission to view this resource.'}), 403
                elif request.method == "DELETE":
                    return jsonify({'error': 'You do not have permission to delete this resource.'}), 403
                elif request.method == "PUT":
                    return jsonify({'error': 'You do not have permission to modify this resource.'}), 403
                else:
                    return abort(403) # if the request method isn't recognized return 403 with no body
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@users_api.cli.command('create-user')
def create():
    username = input('Username: ')
    password = getpass('Password: ')
    admin_role = input('Admin (y/n): ')
    if admin_role == "y":
        admin = True
    elif admin_role == "n":
        admin = False
    else:
        print('Invalid input. Please try again.')
    cur = mysql.connection.cursor()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    try:
        if admin:
            query = cur.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, hashed, 'Administrator'))
        else:
            query = cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed))
        mysql.connection.commit()
    except IntegrityError:
        cur.close()
        print('Error: That user already exists.')
    else:
        cur.close()
        print(f'User {username} successfully created.')


@users_api.route('/', methods=['POST'])
@login_required
@verify_parameters(['username', 'password'])
@roles_required(['Administrator'])
def create_user():
    json = request.get_json()
    cur = mysql.connection.cursor()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(json['password'].encode('utf-8'), salt)
    try:
        query = cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (json['username'], hashed))
        mysql.connection.commit()
    except IntegrityError:
        return jsonify({'error': 'That user already exists.'}), 409

    object = cur.execute('SELECT * FROM users WHERE id = %s', str(cur.lastrowid)) # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'success': 'The user has been successfully created.'})

@users_api.route('/')
@login_required
@roles_required(['Moderator', 'Administrator'])
def users():
    cur = mysql.connection.cursor()
    query = cur.execute('SELECT id,username,active,created_at,updated_at,role FROM users;')
    result = cur.fetchall()
    return jsonify({'users': result})