from flask_restful import Resource
import logging
import json

class Swagger(Resource):
    def get(self):
        logging.info("Displaying swagger json")
        f = open("static/swagger.json").read()
        return json.loads(f)
