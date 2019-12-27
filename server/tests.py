import unittest
from flask_mysqldb import MySQL
from app import app

class PostTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()


    def test_posts(self):
        resp = self.app.get('/api/posts/')

        self.assertEqual(resp.status_code, 200)

    def test_post_unauthorized(self):
        json_data = {'title': 'Test Post', 'slug': 'test_post_unauth', 'body': 'This is a test pos with unauthorized.'}
        resp = self.app.post('/api/posts/', data=json_data)

        self.assertEquals()
if __name__ == "__main__":
    unittest.main()