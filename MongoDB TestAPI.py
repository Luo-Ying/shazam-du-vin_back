from flask import json

from MongoAPI import MongoAPI

if __name__ == '__main__':
    data = {
        "database": "urbanisation",
        "collection": "User",
    }
    mongo_obj = MongoAPI(data)
    print(json.dumps(mongo_obj.read(), indent=4))