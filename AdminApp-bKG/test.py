import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_login_page(self):
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_register_page(self):
        result = self.app.get('/register')
        self.assertEqual(result.status_code, 200)

    def test_admin_panel_requires_login(self):
        result = self.app.get('/admin')
        self.assertEqual(result.status_code, 302)  # Umleitung zur Login-Seite

    def test_404_error(self):
        result = self.app.get('/nonexistent')
        self.assertEqual(result.status_code, 404)

    def test_500_error(self):
        result = self.app.get('/cause_500_error')
        self.assertEqual(result.status_code, 500)

if __name__ == '__main__':
    unittest.main()