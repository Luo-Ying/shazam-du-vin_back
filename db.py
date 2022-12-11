import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')

#This file was the first iteration used to try to create a mongodb connection
#It was later made useless as we switched to another implementation

def get_db():
    """
    Configuration method to return db instance
    """
    db = client['urbanisation']

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
