import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_admin_panel(self):
        result = self.app.get('/admin')
        self.assertEqual(result.status_code, 200)

    def test_subscriptions(self):
        result = self.app.get('/subscriptions')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()