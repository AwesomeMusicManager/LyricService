from os import getenv
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = None


class mongoData:
    def __init__(self, app):
        self.app = app

    def __get_mongo(self):
        global mongo

        if 'MONGO_URI' not in self.app.config:
            mongo_password = getenv("MONGO_PASSWORD", "")
            self.app.config["MONGO_URI"] = "mongodb+srv://admin:{}@cluster0-hb5he.mongodb.net/lyric_service?retryWrites=true&w=majority".format(mongo_password)

        if not mongo:
            mongo = PyMongo(self.app)

        return mongo

    def filter(self, object):
        return self.__get_mongo().db.lyrics.find(object)

    def get_all(self):
        return self.__get_mongo().db.lyrics.find({})

    def add_one(self, data):
        return self.__get_mongo().db.lyrics.insert_one(data)

    def remove_one(self, id):
        return self.__get_mongo().db.lyrics.delete_one({'_id': ObjectId(id)})

    def get_one(self, id):
        return self.__get_mongo().db.lyrics.find_one_or_404(ObjectId(id))


