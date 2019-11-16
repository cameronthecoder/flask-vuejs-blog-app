from flask import Blueprint, request, jsonify, request, g
from .auth import login_required
from json_utils import verify_parameters
from app import app, mysql

users_api = Blueprint('users_api', __name__)

@users_api.route('/', methods=['POST'])
@verify_parameters(['username', 'password'])
@login_required
def create_user():
    json = request.get_json()
    cur = mysql.connection.cursor()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(json['password'].encode('utf-8'), salt)
    try:
        query = cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (json['username'], hashed))
        mysql.connection.commit()
    except MySQLdb._exceptions.IntegrityError:
        return jsonify({'error': 'That user already exists.'}), 409

    object = cur.execute('SELECT * FROM users WHERE id = %s', str(cur.lastrowid)) # return the newly created object back to the user
    result = cur.fetchone()
    cur.close()
    return jsonify({'success': 'The user has been successfully created.'})

@users_api.route('/')
@login_required
def users():
    cur = mysql.connection.cursor()
    query = cur.execute('SELECT * FROM users;')
    result = cur.fetchall()
    users = []
    for user in result:
        users.append({
            'username': user['username'],
            'id': user['id'],
            'active': user['active'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at']
        })
    return jsonify({'users': users})