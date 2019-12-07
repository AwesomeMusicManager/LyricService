from os import getenv
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests
import json

app = Flask(__name__)
api = Api(app)

class HealthCheck(Resource):
    def get(self):
        return "Health check"

class SongLyric(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument("artist", type=str)
        parser.add_argument("song", type=str)

        args = parser.parse_args()

        key = getenv("VAGALUME_LYRIC_API_KEY", "")

        response = requests.get("https://api.vagalume.com.br/search.php?art={artist}&mus={song}&apikey={key}".format(artist=args.artist, song=args.song, key=key)).text
        return json.loads(response)


api.add_resource(HealthCheck, '/')
api.add_resource(SongLyric, '/api/v1/lyrics')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')