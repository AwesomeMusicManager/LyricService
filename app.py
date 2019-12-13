from os import getenv
from flask import Flask, jsonify, abort
from project.health_check import HealthCheck
from project.swagger import Swagger
from project.mongo import mongoData
from flask_restful import Api, Resource, reqparse
import requests
import json
import logging

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger()

song_service_url = getenv("SONG_SERVICE_URL", "https://amm-song-service.herokuapp.com")
logging.info("Started Service")


def handle_request(mongo, args):
    logging.info("Handling request")
    if not args.artist:
        response = requests.get(song_service_url+"/song/{}".format(args.song))

        json_response = json.loads(response.text)

        response = make_request_to_external_api(json_response.get("singer"), json_response.get("name"))
        json_response = json.loads(response)
        return handle_external_api_response(mongo, json_response)
    response = make_request_to_external_api(args.artist, args.song)
    json_response = json.loads(response)
    return handle_external_api_response(mongo, json_response)


def handle_external_api_response(mongo, json_response):
    if json_response.get("type") not in ["song_notfound", "notfound"]:
        logging.info("A song was found")
        obj = json_response["mus"][0]

        insert_new_lyrics(mongo, obj)
        return generate_response(obj["text"])
    return generate_response(json_response)


def make_request_to_external_api(artist, song):
    response = requests.get("https://api.vagalume.com.br/search.php?art={artist}&mus={song}".format(artist=artist,
                                                                                         song=song)).text
    logging.info("Searched for song in external API")
    return response


def generate_response(str):
    logging.info("Generating default response")
    return {"lyric": str}


def insert_new_lyrics(mongo, obj):
    logging.info("Inserting new lyrics to database")
    mongo.add_one({"name": obj["name"], "lyrics": obj["text"]})
    return


class SongLyric(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument("artist", type=str)
        parser.add_argument("song", type=str)

        args = parser.parse_args()

        mongo = mongoData(app)

        if not args.song:
            abort(400, "request should at least contain song parameter")

        get_song = mongo.filter({"name": args.song})
        if get_song.count() >= 1:
            logging.info("Found song lyric in database")
            return generate_response(get_song.next()["lyrics"])

        return handle_request(mongo, args)


class CheckLyricService(Resource):
    def get(self):
        response = requests.get("http://singer-service-app.herokuapp.com").text
        json_response = "Singer service responded with {}".format(jsonify(response))
        logging.info("Healthy")
        return json_response


api.add_resource(HealthCheck, '/')
api.add_resource(Swagger, '/docs')
api.add_resource(CheckLyricService, '/api/v1/singer_check')
api.add_resource(SongLyric, '/api/v1/lyric')


if __name__ == '__main__':
    port = int(getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
