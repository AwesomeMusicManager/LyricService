from flask_restful import Resource
import json

class Swagger(Resource):
    def get(self):
        f = open("static/swagger.json").read()
        return json.loads(f)
