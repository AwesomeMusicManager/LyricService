from flask_restful import Resource
import logging


class HealthCheck(Resource):
    def get(self):
        logging.info("Healthy")
        return "Health Check"
