import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
# client = MongoClient('mongodb+srv://ovhUser:h0Ip6pe9NJnK1EnC@urbanisationceri.vpzkh.mongodb.net/?retryWrites=true&w=majority')


def get_db():
    """
    Configuration method to return db instance
    """
    db = client['urbanisation']

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
