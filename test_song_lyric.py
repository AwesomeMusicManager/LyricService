import unittest

from app import app


class SongLyricTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_making_request_with_no_parameters(self):
        resp = self.client.get(path='/api/v1/lyric', content_type='application/json')
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main