# Flask REST API with JWT Authentication

---
# Todo
- [x] Split into different route files (Flask Blueprints)
- [x] Add edit post route
- [x] Check if the JSON contains the keys needed
- [ ] Roles / permissions
- [ ] Delete / View users
- [ ] Auto-gen. slug
## Requirements
1. Via ```pip``` package manager
    * Flask
    * Flask-MySQLdb
    * bcrypt
    * pyjwt
2. Other 
    * MySQL Database
    * Python 3
## Notes
* The MySQL user table contains a password field and it needs to be of type ``CHAR 60 BINARY``
* Make sure to setup all of the enviornment variables before running the application.
