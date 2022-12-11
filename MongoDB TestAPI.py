from flask import json

from MongoAPI import MongoAPI

if __name__ == '__main__':
    data = {
        "database": "urbanisation",
        "collection": "User",
    }
    mongo_obj = MongoAPI(data)
    print(json.dumps(mongo_obj.read(), indent=4))

#Same as db.py it is a test file that was made in the ealry days of the app to test how mongo and flask could work together