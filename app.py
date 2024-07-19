from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['flask_items']
collection = db['items']

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    result = collection.insert_one(data);
    return jsonify({ '_id': str(result.inserted_id)}), 201

@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items), 200

@app.route('/item/<id>', methods=['GET'])
def get_item(id):
    try:
        item = collection.find_one({'_id': ObjectId(id)})
        if item:
            item['_id'] = str(item['_id'])
            return jsonify(item), 200
        return jsonify({ 'error': 'Item not found' }), 404
    except:
        return jsonify({'error': 'Invalid ID format'}), 400

@app.route('/item/<id>', methods=['PUT'])
def update_item(id):
    try:
        data = request.json
        result = collection.update_one({ '_id': ObjectId(id) }, { '$set': data })
        if result.matched_count:
            return jsonify({'message': 'Item updated successfully'}), 200
        return jsonify({'error': 'Item not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID format'}), 400

@app.route('/item/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({'message': 'Item deleted successfully'}), 200
        return jsonify({ 'error': 'Item not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID format'}), 400

if __name__ == '__main__':
    app.run(debug=True)