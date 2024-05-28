from flask import request, jsonify
from flask.views import MethodView
from flask_socketio import SocketIO, emit
from bson.objectid import ObjectId
from db import db

socketio = SocketIO()

"""
TODO: fix and do some sort of conversations collection
"""
class MessageView(MethodView):
    def __init__(self):
        self.collection = db['messages']
    
    def get(self, id=None):
        if id is None:
            messages = list(self.collection.find())
            for message in messages:
                message['_id'] = str(message['_id'])
            return jsonify(messages), 200
        else:
            message = self.collection.find_one({'_id': ObjectId(id)})
            if message:
                message['_id'] = str(message['_id'])
                return jsonify(message), 200
            else:
                return jsonify({'error': 'Message not found'}), 404

    def post(self):
        data = request.get_json()
        result = self.collection.insert_one(data)
        message_id = str(result.inserted_id)
        socketio.emit('new_message', {'_id': message_id, **data}, broadcast=True)
        return jsonify({'_id': message_id}), 201

    def put(self, id):
        data = request.get_json()
        result = self.collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count > 0:
            socketio.emit('update_message', {'_id': id, **data}, broadcast=True)
            return jsonify({'message': 'Message updated successfully'}), 200
        else:
            return jsonify({'error': 'Message not found'}), 404

    def delete(self, id):
        result = self.collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            socketio.emit('delete_message', {'_id': id}, broadcast=True)
            return jsonify({'message': 'Message deleted successfully'}), 200
        else:
            return jsonify({'error': 'Message not found'}), 404