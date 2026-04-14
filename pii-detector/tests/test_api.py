import unittest
from backend.api import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_and_scan(self):
        response = self.app.post('/api/upload', data={'file': (open('test_file.txt', 'rb'), 'test_file.txt')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('PII Found', response.get_data(as_text=True))

    def test_manual_input_analysis(self):
        response = self.app.post('/api/analyze', json={'text': 'My email is example@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('PII Found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()