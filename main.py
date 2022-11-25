from flask import Flask, Response, json
from flask import request
from MongoAPI import *

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/getUsers")
def getUsers():
    db = get_db()
    print(db.get_collection('User').find())
    return ":)"

@app.route("/getUser", methods=['POST'])
def getUser():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        obj1 = MongoAPI(data)
        response = obj1.read()
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')

    if data and 'Filter' in data:
        obj1 = MongoAPI(data)
        response = obj1.readWith()
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')


@app.route('/User', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user_crud():
    if request.method == 'POST':
        data = request.json
        if data is None or data == {} or 'Document' not in data:
            return Response(response=json.dumps({"Error": "Please provide connection information"}),
                            status=400,
                            mimetype='application/json')
        obj1 = MongoAPI(data)
        response = obj1.write(data)
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')

    if request.method == 'PUT':
        data = request.json
        if data is None or data == {} or 'DataToBeUpdated' not in data:
            return Response(response=json.dumps({"Error": "Please provide connection information"}),
                            status=400,
                            mimetype='application/json')
        obj1 = MongoAPI(data)
        response = obj1.update()
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')

    if request.method == 'DELETE':
        data = request.json
        if data is None or data == {} or 'Filter' not in data:
            return Response(response=json.dumps({"Error": "Please provide connection information"}),
                            status=400,
                            mimetype='application/json')
        obj1 = MongoAPI(data)
        response = obj1.delete(data)
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')


    if request.method == 'GET':
        print("request: ", request)
        data = request.json
        print("data: ", data)
        if data is None or data == {} or 'Filter' not in data:
            obj1 = MongoAPI(data)
            response = obj1.read()
            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')

        if data and 'Filter' in data:
            obj1 = MongoAPI(data)
            response = obj1.readWith()
            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')

@app.route("/searchWineByImg")
def getWinesByImg():
    return "<p>Super</p>"
