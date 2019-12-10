from os import getenv
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import json

app = Flask(__name__)
api = Api(app)

mongo_password = getenv("MONGO_PASSWORD", "")

app.config['MONGO_URI'] = "mongodb+srv://admin:{}@cluster0-hb5he.mongodb.net/lyric_service?retryWrites=true&w=majority".format(mongo_password)

mongo = PyMongo(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Lyric Service"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

class HealthCheck(Resource):
    def get(self):
        return "Health check"

class SongLyric(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument("artist", type=str)
        parser.add_argument("song", type=str)

        args = parser.parse_args()

        get_song = mongo.db.lyrics.find({"name": args.song})

        if get_song.count() >= 1:
            return get_song.next()["lyrics"]
        else:
            response = requests.get("https://api.vagalume.com.br/search.php?art={artist}&mus={song}".format(artist=args.artist, song=args.song)).text

            json_response = json.loads(response)
            if json_response.get("type") not in ["song_notfound", "notfound"]:
                obj = json_response["mus"][0]

                mongo.db.lyrics.insert_one({"name": obj["name"], "lyrics": obj["text"]})
                return obj["text"]
            return json_response
            

api.add_resource(HealthCheck, '/')
api.add_resource(SongLyric, '/api/v1/get_lyric')

if __name__ == '__main__':
    port = int(getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0',port=port)