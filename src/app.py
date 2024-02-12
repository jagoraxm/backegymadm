from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
# importing ObjectId from bson library
from bson.objectid import ObjectId

app =  Flask(__name__)

CORS(app)

uri = "mongodb://localhost:27017"

try: 
    conn = MongoClient(uri)
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 
    
db = conn.mousegym

collection = db.users

@app.route('/graph', methods=['POST'])
def createGRaphs():
    response = {
        'data': ''
    }
    return jsonify(response)

@app.route('/signin', methods=['POST'])
def signIn():
    user = collection.find_one({"name": request.json['username']})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

@app.route('/users', methods=['POST'])
def createUser():
    _id = collection.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    print(_id.inserted_id)
    response = {
        'data': str(_id.inserted_id)
    }
    return jsonify(response)

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for document in collection.find():
        users.append({
            '_id': str(document['_id']),
            'name': document['name'],
            'email': document['email'],
            'password': document['password']
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = collection.find_one({"_id": ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "usuario eliminado"})

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    collection.update_one({"_id": ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({"msg": "usuario actualizado"})

if __name__ == "__main__":
    app.run(debug=True)