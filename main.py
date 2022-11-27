import os
from uuid import uuid4

from flask import Flask, Response, json, redirect
from flask import request
from MongoAPI import *
import boto3

UPLOAD_FOLDER = './upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    s3 = boto3.resource("s3")
    test = boto3.client('s3')

    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
    return "<p>Hello, World!</p><br/>"

'''
@app.route("/testIMG", methods=['GET', 'POST'])
def test_img():
    # image = request.files.get('image', '')
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = uuid4()
        extension = file.filename.rsplit('.', 1)[1].lower()
        filename = str(filename) + '.' + extension
        s3 = boto3.client('s3')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = "upload/"+filename
        with open(filepath, "rb") as f:
            s3.upload_fileobj(f, "urbanisationceriperso", filename, ExtraArgs={'ContentType': "image/"+extension, 'ACL': 'public-read'})
        url = f'https://urbanisationceriperso.s3.eu-west-3.amazonaws.com/{filename}'
        return url
'''

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
        if request.args.get('username'):
            data = {
                "database": "urbanisation",
                "collection": "User",
                "filter": {
                    "username": request.args.get('username'),
                    "password": request.args.get('password')
                }
            }
        else:
            data = {
                "database": "urbanisation",
                "collection": "User"
            }
            
        if data is None or data == {} or 'filter' not in data:
            obj1 = MongoAPI(data)
            response = obj1.read()
            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')

        if data and 'filter' in data:
            obj1 = MongoAPI(data)
            response = obj1.readWith()

            exist = json.dumps(response)
            print(exist)
            if exist.find("username") == "":
                return Response(response=json.dumps(response),
                                status=401,
                                mimetype='application/json')

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
        data = {
            "database": "urbanisation",
            "collection": "Vin",
            "filter": {
                "username": request.args.get('username'),
                "password": request.args.get('password')
            }
        }
        if data is None or data == {} or 'filter' not in data:
            obj1 = MongoAPI(data)
            response = obj1.read()
            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')

        if data and 'filter' in data:
            obj1 = MongoAPI(data)
            response = obj1.readWith()

            exist = json.dumps(response)
            print(exist)
            if exist.find("username") == "":
                return Response(response=json.dumps(response),
                                status=401,
                                mimetype='application/json')

            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')



@app.route('/top', methods=['GET'])
def top10():
    if request.method == 'GET':
        data = {
                   "database": "urbanisation",
                   "collection": "User"
        }
        obj1 = MongoAPI(data)
        response = obj1.readWith()
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')

@app.route('/insertImg', methods=['POST'])
def img_post():
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = uuid4()
        extension = file.filename.rsplit('.', 1)[1].lower()
        filename = str(filename) + '.' + extension
        s3 = boto3.client('s3')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = "upload/" + filename
        with open(filepath, "rb") as f:
            s3.upload_fileobj(f, "urbanisationceriperso", filename,
                              ExtraArgs={'ContentType': "image/" + extension, 'ACL': 'public-read'})
        url = f'https://urbanisationceriperso.s3.eu-west-3.amazonaws.com/{filename}'
        return url

