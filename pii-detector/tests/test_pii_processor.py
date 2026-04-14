import unittest
from backend.services.pii_processor import detect_pii

class TestPIIProcessor(unittest.TestCase):

    def test_detect_pii_email(self):
        text = "My email is example@example.com."
        expected_output = ["example@example.com"]
        self.assertEqual(detect_pii(text), expected_output)

    def test_detect_pii_phone(self):
        text = "Call me at (123) 456-7890."
        expected_output = ["(123) 456-7890"]
        self.assertEqual(detect_pii(text), expected_output)

    def test_detect_pii_ssn(self):
        text = "My social security number is 123-45-6789."
        expected_output = ["123-45-6789"]
        self.assertEqual(detect_pii(text), expected_output)

    def test_no_pii(self):
        text = "This is a regular sentence without sensitive information."
        expected_output = []
        self.assertEqual(detect_pii(text), expected_output)

    def test_detect_multiple_pii(self):
        text = "My email is example@example.com and my phone number is (123) 456-7890."
        expected_output = ["example@example.com", "(123) 456-7890"]
        self.assertEqual(detect_pii(text), expected_output)

if __name__ == '__main__':
    unittest.main()