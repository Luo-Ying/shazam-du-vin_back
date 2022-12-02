import os
import io
from uuid import uuid4

from flask import Flask, Response, json, redirect
from flask import request
from MongoAPI import *
import boto3
import re
from unidecode import unidecode

UPLOAD_FOLDER = './upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def healthcheck():
    return "OK!"


@app.route("/testBucket")
def hello_world():
    s3 = boto3.resource("s3")
    test = boto3.client('s3',
                        aws_access_key_id="AKIA6JLBSVCU7FDCKX4U",
                        aws_secret_access_key="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"
                        )

    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
    return "<p>Hello, World!</p><br/>"


@app.route('/User', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user_crud():
    if request.method == 'POST':
        data = request.json
        if data is None or data == {} or 'data' not in data:
            return Response(response=json.dumps({"Error": "Please provide connection information"}),
                            status=400,
                            mimetype='application/json')

        dataTest = {
            "database": "urbanisation",
            "collection": "User",
            "filter": {
                "username": data['data']["username"]
            }
        }
        obj2 = MongoAPI(dataTest)
        res = obj2.readWith()
        print(res)
        print(len(res))
        if len(res) > 0:
            return Response(response=json.dumps({"Error": "User already exist with this username"}),
                            status=401,
                            mimetype='application/json')
        dataFinal = {
            "database": "urbanisation",
            "collection": "User",
            "data": data["data"]
        }
        obj1 = MongoAPI(dataFinal)
        response = obj1.write(data)
        print(dataFinal)
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
            if request.args.get('password'):
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
        else:
            data = {
                "database": "urbanisation",
                "collection": "User"
            }

        print(data)

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
            print(len(exist))
            if len(exist) <= 2:
                return Response(response=json.dumps(response),
                                status=401,
                                mimetype='application/json')

            delim = exist.split(',', 1)[1]
            delim = delim.split(']', 1)[0]
            delim = delim.split(' ', 1)[1]
            delim = '{' + delim + '}}'
            print(delim)
            return Response(response=json.dumps(exist),
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
        if request.args.get('nom'):
            data = {
                "database": "urbanisation",
                "collection": "Vin",
                "filter": {
                    "id": request.args.get('nom')
                }
            }
        elif request.args.get('id'):
            data = {
                "database": "urbanisation",
                "collection": "Vin",
                "filter": {
                    "id": request.args.get('id')
                }
            }
        else:
            data = {
                "database": "urbanisation",
                "collection": "Vin"
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
            if exist.find("nom") == "":
                return Response(response="Error 404 Not foud",
                                status=404,
                                mimetype='application/json')

            return Response(response=json.dumps(response),
                            status=200,
                            mimetype='application/json')


@app.route('/top', methods=['GET'])
def top10():
    if request.method == 'GET':
        data = {
            "database": "urbanisation",
            "collection": "Vin"
        }
        obj1 = MongoAPI(data)
        response = obj1.readTop()
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
        s3 = boto3.client('s3',
                          aws_access_key_id="AKIA6JLBSVCU7FDCKX4U",
                          aws_secret_access_key="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"
                          )
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = "upload/" + filename
        with open(filepath, "rb") as f:
            s3.upload_fileobj(f, "urbanisationceriperso", filename,
                              ExtraArgs={'ContentType': "image/" + extension, 'ACL': 'public-read'})
        url = f'https://urbanisationceriperso.s3.eu-west-3.amazonaws.com/{filename}'
        return url


@app.route('/ocr', methods=['POST'])
def orm_endpoint():
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = uuid4()
        extension = file.filename.rsplit('.', 1)[1].lower()
        filename = str(filename) + '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = "upload/" + filename

        # Read document content
        with open(filepath, 'rb') as document:
            imageBytes = bytearray(document.read())

        # Amazon Textract client
        textract = boto3.client('textract',
                                aws_access_key_id="AKIA6JLBSVCU7FDCKX4U",
                                aws_secret_access_key="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")

        # Call Amazon Textract
        response = textract.detect_document_text(Document={'Bytes': imageBytes})

        # print(response)

        formatedResponse = []
        listVin = []

        # Print detected text
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                print('\033[94m' + item["Text"] + '\033[0m')
                formatedResponse.append(item["Text"])

        for item in formatedResponse:
            if item.find('vivino') != -1 or item.find('VIVINO') != -1 or item.find('Vivino') != -1:
                del formatedResponse[-1]

        formatedResponse = [item for item in formatedResponse if len(item) > 2]

        decodeResponse = []

        for item in formatedResponse:
            decodeResponse.append(unidecode(item))

        print(decodeResponse)

        for item in decodeResponse:
            print(item)
            data = {
                "database": "urbanisation",
                "collection": "Vin"
            }
            query = {
                "nom": {
                    "$regex": '^.*' + item + '.*',
                    "$options": 'i'  # case-insensitive
                }
            }
            obj1 = MongoAPI(data)
            documents = obj1.collection.find(query)
            response = [{item: data[item] for item in data if item != '_id'} for data in documents]
            listVin.append(response)

        print(listVin)
        setOfElement = []
        listOfId = list()
        for response in listVin:
            for data in response:
                if data["id"] not in listOfId:
                    listOfId.append(data["id"])
                    setOfElement.append(data)

        print(listOfId)
        print(setOfElement)

        return Response(response=json.dumps(setOfElement),
                    status=200,
                    mimetype='application/json')

    return "NOT OK"


@app.route('/searchL', methods=['GET'])
def search_levenshtein():
    data = {
        "database": "urbanisation",
        "collection": "Vin"
    }

    query = {
        "nom": {
            "$regex": '^.*Rhône.*',
            "$options": 'i'  # case-insensitive
        }
    }

    obj1 = MongoAPI(data)
    documents = obj1.collection.find(query)
    response = [{item: data[item] for item in data if item != '_id'} for data in documents]
    setOfElement = []
    listOfId = list()
    for data in response:
        if data["id"] not in listOfId:
            listOfId.append(data["id"])
            setOfElement.append(data)

    print(setOfElement)
    print(listOfId)

    return Response(response=json.dumps(setOfElement),
                    status=200,
                    mimetype='application/json')


@app.route('/favVin', methods=['GET'])
def fav_vin():
    if request.method == 'GET':
        if request.args.get('username'):
            data = {
                "database": "urbanisation",
                "collection": "User",
                "filter": {
                    "username": request.args.get('username')
                }
            }

            print(data)

            obj1 = MongoAPI(data)
            res = obj1.readWith()

            print(res[0]['vinFav']['value'])

            vins = res[0]['vinFav']['value']

            if len(vins) == 0:
                return Response(response=json.dumps({}),
                                status=200,
                                mimetype='application/json')

            listVins = []

            for item in vins:
                data2 = {
                    "database": "urbanisation",
                    "collection": "Vin",
                    "filter": {
                        "id": item
                    }
                }
                obj2 = MongoAPI(data2)
                temp = obj2.readWith()
                if len(temp) > 0:
                    listVins.append(temp)

            return Response(response=json.dumps(listVins),
                            status=200,
                            mimetype='application/json')

    return Response(response=json.dumps({"Error": "Bad Request"}),
                    status=400,
                    mimetype='application/json')

#TODO: - enpoint '/favVin'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
