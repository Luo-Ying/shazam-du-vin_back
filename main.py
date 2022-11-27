from flask import Flask, Response, json
from flask import request
from MongoAPI import *
import boto3

app = Flask(__name__)


@app.route("/")
def hello_world():
    s3 = boto3.resource("s3")
    test = boto3.client('s3')

    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
    return "<p>Hello, World!</p><br/>"


@app.route("/testIMG", methods=['GET', 'POST'])
def test_img():
    # image = request.files.get('image', '')
    image = request.files["image"]
    filename = image.filename
    data = request.values.get('imageName')
    print(image)
    print(json.dumps(data))
    s3 = boto3.client('s3')
    with open(image, "rb") as f:
        s3.upload_fileobj(f, "urbanisationceriperso", filename, ExtraArgs={'ACL': 'public-read'})
    return "<p>Nice</p>"


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
        if data is None or data == {} or 'data' not in data:
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
        if data is None or data == {} or 'data' not in data:
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
        if data is None or data == {} or 'filter' not in data:
            return Response(response=json.dumps({"Error": "Please provide connection information"}),
                            status=400,
                            mimetype='application/json')
        obj1 = MongoAPI(data)
        response = obj1.delete(data)
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')

    if request.method == 'GET':
        data = request.json
        if data is None or data == {} or 'filter' not in data:
            obj1 = MongoAPI(data)
            response = obj1.read()

            exist = json.dumps(response)
            if (exist["username"] == ""):
                return Response(response=json.dumps(response),
                                status=401,
                                mimetype='application/json')

            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')

        if data and 'filter' in data:
            obj1 = MongoAPI(data)
            response = obj1.readWith()
            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')


@app.route('/Vin', methods=['GET', 'POST', 'DELETE', 'PUT'])
def vin_crud():
    if request.method == 'POST':
        data = request.json
        if data is None or data == {} or 'data' not in data:
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
        if data is None or data == {} or 'data' not in data:
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
        if data is None or data == {} or 'filter' not in data:
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
