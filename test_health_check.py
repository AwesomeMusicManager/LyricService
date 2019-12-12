import unittest

import app


class HealthCheckTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_making_health_check(self):
        resp = self.client.get(path='/', content_type='application/json')
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main