from flask_pymongo import PyMongo

mongo = PyMongo()


def init_app(app):
    return mongo.init_app(app)
