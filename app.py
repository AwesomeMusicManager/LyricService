from os import getenv
from flask import Flask, jsonify
from project.health_check import HealthCheck
from project.swagger import Swagger
from project.mongo import mongoData
from flask_restful import Api, Resource, reqparse
import requests
import json
import logging

app = Flask(__name__)
api = Api(app)

logging.basicConfig(filename="logFile.txt",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("Started Service")


class SongLyric(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument("artist", type=str)
        parser.add_argument("song", type=str)

        args = parser.parse_args()

        mongo = mongoData(app)

        get_song = mongo.filter({"name": args.song})

        if get_song.count() >= 1:
            logging.info("Found song lyric in database")
            return get_song.next()["lyrics"]
        else:
            response = requests.get("https://api.vagalume.com.br/search.php?art={artist}&mus={song}".format(artist=args.artist, song=args.song)).text
            logging.info("Searched for song in API")

            json_response = json.loads(response)
            if json_response.get("type") not in ["song_notfound", "notfound"]:
                logging.info("A song was found")
                obj = json_response["mus"][0]

                mongo.add_one({"name": obj["name"], "lyrics": obj["text"]})
                return obj["text"]
            return json_response


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
