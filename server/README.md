# Flask REST API with JWT Authentication

---
# TODO
- [x] Split routes into different files (Flask Blueprints)
- [x] Add edit post route
- [x] Check if the JSON contains the keys needed
  - [x] Add a decorator to simplify the route function instead of checking every time
  ```python
  # Example API route
  @posts_api.route('/', methods=['POST'])
  @login_required
  @json_required(['title', 'body', 'slug'])
  def create_post():
      # ...
  ```    
- [x] Use prepared statements
- [x] Add author_id and draft to the posts schema
- [x] Refresh tokens for better UX (I hope I have implemented this correctly, please let me know if I haven't.)
- [ ] Roles / permissions
- [ ] Implement tests
- [ ] Automatic table creation
- [ ] Delete / View users
- [ ] Auto-gen. slug
- [ ] VueJS front-end
## Contributions
I am open to anyone submitting a pull request or issue if you want to improve, make a suggestion, or add to my code 😀.
## Running the app
1. Install MySQL
   * [Ubuntu](https://help.ubuntu.com/lts/serverguide/mysql.html)
   * [Windows](https://dev.mysql.com/downloads/installer/)
   * [MacOS (Two different options)](https://dev.mysql.com/doc/mysql-osx-excerpt/5.7/en/osx-installation.html)
   ---
    1. Log into the MySQL server and create a database
    ```sql
    CREATE DATABASE <name>
    ```
    2. Use the newly created database
    ```sql
    USE <name>
    ```
    3. Create the tables using [create_posts.sql](create_posts.sql) and [create_users.sql](create_users.sql) (will be automated later)
    4. Exit MySQL (```exit```)
    5. **Important: If you're using Ubuntu (or a similar OS) make sure you install the ```libmysqlclient-dev``` package, if you don't the pip command will result in an ```OSError``` error.**
2. Create a Python virtual enviornment and activate it:
```
python3 -m venv env
source env/bin/activate
```
3. Install the required packages via ```pip``` (if you're using a virtual env.) or ```pip3```:
```
pip install -r requirements.txt
```
4. Set your enviornment variables:
   * MYSQL_USER
   * MYSQL_PASSWORD
   * MYSQL_DB
   * APP_SECRET_KEY
   * FLASK_APP (optional, use if you plan on using ```flask run```)
   * FLASK_DEBUG (optional)
5. Run the app:
```
flask run
```
or
```
python3 app.py
```
6. Create a user:
```
flask create-user
Username: <username>
Password: <password>
User <username> successfully created.
```
or
```
python3 app.py create-user
Username: <username>
Password: <password>
User <username> successfully created.
```