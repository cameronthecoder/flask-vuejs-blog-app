# Flask REST API with JWT Authentication

---
# TODO
- [x] Split routes into different files (Flask Blueprints)
- [x] Add edit post route
- [x] Check if the JSON contains the keys needed
  - [x] Add a decorator to simplify the route function instead of checking every time?
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
- [x] Refresh tokens for better UX (I hope I have implemented this correctly, please let me know if I have not.)
- [ ] Roles / permissions
- [ ] Implement tests
- [ ] Automatic table creation
- [ ] Delete / View users
- [ ] Auto-gen. slug
- [ ] VueJS front-end
## Requirements
1. Via ```pip``` package manager
    * Flask
    * Flask-MySQLdb
    * bcrypt
    * pyjwt
    * Flask-CORS
2. Other 
    * MySQL Database
    * Python 3
