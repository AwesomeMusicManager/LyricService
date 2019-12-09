import os
import tempfile
from flask import Flask, request
import app
from unittest import TestCase

import pytest


app = Flask(__name__)

# @app.route('/')
# def test_heath_check2():
#     json_data = request.get_json()
#     print(json_data)
# with app.test_health_check() as c:
#     rv = c.get('/')
#     json_data = rv.get_json()
#     print(json_data)


class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_thing(self):
        response = self.app.get('/api/v1/get_lyric?artist=MFDOOM&song=Doomsday')
        assert response.status == '200'