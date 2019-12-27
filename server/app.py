from flask import Flask
from flask_mysqldb import MySQL
from json_utils import CustomJSONEncoder
from flask_cors import CORS
import os

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder # custom JSON encoder so the time stamps are formatted in the ISO format
mysql = MySQL(app)
CORS(app)
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']

from routes.users import users_api
from routes.auth import auth_api
from routes.posts import posts_api
app.register_blueprint(auth_api, url_prefix='/api/auth')
app.register_blueprint(posts_api, url_prefix='/api/posts')
app.register_blueprint(users_api, url_prefix='/api/users')

if __name__ == "__main__":
    app.run(debug=True)