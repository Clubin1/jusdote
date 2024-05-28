from flask import request, jsonify
from flask.views import MethodView
from db import db
from bson.objectid import ObjectId
import boto3

class FileView(MethodView):
    def __init__(self) -> None:
        self.collection = db['files']
        self.folder_collection = db['folders']
        self.s3 = boto3.client('s3')
        self.bucket_name = 'your-bucket-name'  # Replace with your S3 bucket name

    def post(self, folder_id):
        folder = self.folder_collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return jsonify({'error': 'Folder not found'}), 404

        user_id = request.args.get('user_id')  # Assuming user_id is obtained from authentication
        if not self.has_permission(folder, user_id, role='editor'):
            return jsonify({'error': 'Unauthorized access'}), 403

        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        filename = file.filename

        # Upload the file to S3
        self.s3.upload_fileobj(file, self.bucket_name, filename)

        # Create a file metadata document in MongoDB
        file_metadata = {
            'filename': filename,
            'folder_id': folder_id,
            'size': file.content_length,
            'content_type': file.content_type,
            # Add any other relevant metadata fields
        }
        result = self.collection.insert_one(file_metadata)
        file_id = str(result.inserted_id)

        # Update the folder document to include the file reference
        self.folder_collection.update_one(
            {'_id': ObjectId(folder_id)},
            {'$push': {'files': file_id}}
        )

        return jsonify({'file_id': file_id}), 201

    def get(self, file_id):
        file_metadata = self.collection.find_one({'_id': ObjectId(file_id)})
        if not file_metadata:
            return jsonify({'error': 'File not found'}), 404

        folder_id = file_metadata['folder_id']
        folder = self.folder_collection.find_one({'_id': ObjectId(folder_id)})

        user_id = request.args.get('user_id')  # Assuming user_id is obtained from authentication
        if not self.has_permission(folder, user_id):
            return jsonify({'error': 'Unauthorized access'}), 403

        # Generate a presigned URL for downloading the file from S3
        presigned_url = self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': file_metadata['filename']},
            ExpiresIn=3600  # URL expiration time in seconds
        )

        file_metadata['_id'] = str(file_metadata['_id'])
        file_metadata['folder_id'] = str(file_metadata['folder_id'])
        return jsonify({
            'metadata': file_metadata,
            'download_url': presigned_url
        }), 200

    def has_permission(self, folder, user_id, role='viewer'):
        for permission in folder['permissions']:
            if permission['user_id'] == user_id and permission['role'] in ['owner', role]:
                return True
        return False