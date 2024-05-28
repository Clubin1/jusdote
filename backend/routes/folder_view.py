from flask import request, jsonify
from flask.views import MethodView
from db import db
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity

class Folder(MethodView):
    def __init__(self) -> None:
        self.collection = db['folders']

    @jwt_required()
    def post(self):
        data = request.get_json()
        folder_name = data.get("name")
        user_id = get_jwt_identity()
        if not folder_name or not user_id:
            return jsonify({"error": "Please enter a valid name or user_id"}), 400

        folder = {
            "name": folder_name,
            "owner": user_id,
            "files": [],
            "permissions": [{
                "user_id": user_id,
                "role": "owner"
            }]
        }
        result = self.collection.insert_one(folder)
        folder_id = str(result.inserted_id)
        return jsonify({"folder_id": folder_id}), 201
    
    @jwt_required()
    def get_user_folders(self):
        user_id = get_jwt_identity()
        folders = list(self.collection.find({'user_id': user_id}))
        for folder in folders:
            folder['_id'] = str(folder['_id'])
        return jsonify(folders), 200
    
    @jwt_required()
    def get_single_folder(self, folder_id):
        user_id = get_jwt_identity()
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return jsonify({'error': 'Folder not found'}), 404
        
        if not self.has_permission(folder, user_id):
            return jsonify({'error': 'Unauthorized access'}), 403
        
        folder['_id'] = str(folder['_id'])
        return jsonify(folder), 200

    def has_permission(self, folder, user_id, role='viewer'):
        if folder['owner'] == user_id:
            return True
        for permission in folder['permissions']:
            if permission['user_id'] == user_id and permission['role'] in ['owner', role]:
                return True
        return False