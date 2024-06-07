from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit
from bson.objectid import ObjectId
import boto3
from flask_cors import CORS
from db import db

app = Flask(__name__)
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})
# AWS S3 configuration
s3 = boto3.client(
    's3',
    aws_access_key_id='your_aws_access_key_id',
    aws_secret_access_key='your_aws_secret_access_key'
)
bucket_name = 'your_bucket_name'

# Routes


@app.route('/')
def home():
    return 'Hello, World!'

# Auth


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    if not username or not password or not role:
        return jsonify({"error": "Please provide a valid username, password, and role"}), 400
    collection = db['users']
    existing_user = collection.find_one({"username": username})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {'username': username, 'password': hashed_password, 'role': role}
    collection.insert_one(user)
    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    collection = db['users']
    user = collection.find_one({'username': username})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=str(
        user['_id']))  # Pass the user ID as the identity
    return jsonify({'access_token': access_token, 'userId': str(user['_id'])}), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! This is a protected endpoint.'}), 200


@app.route('/api/user-info', methods=['GET'])
@jwt_required()
def user_info():
    current_user = get_jwt_identity()
    collection = db['users']
    user = collection.find_one({'username': current_user})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_info = {
        'username': user['username'],
        'role': user['role']
    }
    return jsonify(user_info), 200

# Admin


@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    collection = db['admins']
    user = collection.find_one({'username': username})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200


@app.route('/admin/active-applications', methods=['GET'])
@jwt_required
def get_active_applications():
    collection = db['client_applications']
    active_applications = list(collection.find({'active': True}))
    for app in active_applications:
        app['_id'] = str(app['_id'])
    return jsonify(active_applications), 200

# Client Applications


@app.route('/api/client/applications', methods=['POST'])
@jwt_required()
def create_client_application():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    data['userId'] = current_user_id
    collection = db['client_applications']
    result = collection.insert_one(data)
    application_id = str(result.inserted_id)
    return jsonify({'_id': application_id}), 201


@app.route('/api/client/applications', methods=['GET'])
@jwt_required()
def get_client_applications():
    current_user_id = get_jwt_identity()
    collection = db['client_applications']
    applications = list(collection.find({'userId': current_user_id}))
    for app in applications:
        app['_id'] = str(app['_id'])
    return jsonify(applications), 200


@app.route('/api/client/applications/<id>', methods=['PUT'])
@jwt_required()
def update_client_application(id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    collection = db['client_applications']
    result = collection.update_one(
        {'_id': ObjectId(id), 'user_id': current_user_id}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Application updated successfully'}), 200
    else:
        return jsonify({'error': 'Application not found'}), 404


@app.route('/api/client/applications/<id>', methods=['DELETE'])
@jwt_required()
def delete_client_application(id):
    current_user_id = get_jwt_identity()
    collection = db['client_applications']
    result = collection.delete_one(
        {'_id': ObjectId(id), 'user_id': current_user_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Application deleted successfully'}), 200
    else:
        return jsonify({'error': 'Application not found'}), 404

# Editor Applications


@app.route('/api/editor/applications', methods=['POST'])
@jwt_required()
def create_editor_application():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    data['userId'] = current_user_id
    collection = db['editor_applications']
    result = collection.insert_one(data)
    application_id = str(result.inserted_id)
    return jsonify({'_id': application_id}), 201


@app.route('/api/editor/applications', methods=['GET'])
@jwt_required()
def get_editor_applications():
    current_user_id = get_jwt_identity()
    collection = db['editor_applications']
    applications = list(collection.find({'userId': current_user_id}))
    for app in applications:
        app['_id'] = str(app['_id'])
    return jsonify(applications), 200


@app.route('/api/editor/applications/<id>', methods=['PUT'])
@jwt_required()
def update_editor_application(id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    collection = db['editor_applications']
    result = collection.update_one(
        {'_id': ObjectId(id), 'user_id': current_user_id}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Application updated successfully'}), 200
    else:
        return jsonify({'error': 'Application not found'}), 404


@app.route('/api/editor/applications/<id>', methods=['DELETE'])
@jwt_required()
def delete_editor_application(id):
    current_user_id = get_jwt_identity()
    collection = db['editor_applications']
    result = collection.delete_one(
        {'_id': ObjectId(id), 'user_id': current_user_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Application deleted successfully'}), 200
    else:
        return jsonify({'error': 'Application not found'}), 404

# Folders


@app.route('/api/folders', methods=['POST'])
@jwt_required()
def create_folder():
    data = request.get_json()
    folder_name = data.get("name")
    user_id = get_jwt_identity()
    if not folder_name or not user_id:
        return jsonify({"error": "Please enter a valid name or user_id"}), 400
    collection = db['folders']
    folder = {
        "name": folder_name,
        "owner": user_id,
        "files": [],
        "permissions": [{
            "user_id": user_id,
            "role": "owner"
        }]
    }
    result = collection.insert_one(folder)
    folder_id = str(result.inserted_id)
    return jsonify({"folder_id": folder_id}), 201


@app.route('/api/folders', methods=['GET'])
@jwt_required()
def get_user_folders():
    user_id = get_jwt_identity()
    collection = db['folders']
    folders = list(collection.find({'owner': user_id}))
    for folder in folders:
        folder['_id'] = str(folder['_id'])
    return jsonify(folders), 200


@app.route('/api/folders/<folder_id>', methods=['GET'])
@jwt_required()
def get_single_folder(folder_id):
    user_id = get_jwt_identity()
    collection = db['folders']
    folder = collection.find_one({'_id': ObjectId(folder_id)})
    if not folder:
        return jsonify({'error': 'Folder not found'}), 404
    if not has_permission(folder, user_id):
        return jsonify({'error': 'Unauthorized access'}), 403
    folder['_id'] = str(folder['_id'])
    return jsonify(folder), 200


@app.route('/api/folders/<folder_id>/add_permission', methods=['POST'])
@jwt_required()
def add_permission(folder_id):
    # look up user id and if it doesnt exist return error
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or 'user_id' not in data or 'role' not in data:
        return jsonify({'error': 'Missing user_id or role'}), 400

    user_to_add_id = data.get("user_id")
    role = data.get("role")
    collection = db['folders']
    folder = collection.find_one({'_id': ObjectId(folder_id)})
    if not folder:
        return jsonify({'error': 'Folder not found'}), 404

    if 'permissions' not in folder:
        folder['permissions'] = []

    folder['permissions'].append({"user_id": user_to_add_id, "role": role})
    collection.update_one({'_id': ObjectId(folder['_id'])}, {
                          '$set': {'permissions': folder['permissions']}})

    folder['_id'] = str(folder['_id'])

    return jsonify(folder), 200


def has_permission(folder, user_id):
    if folder['owner'] == user_id:
        return True
    for permission in folder['permissions']:
        if permission['user_id'] == user_id and permission['role'] in ['owner', 'viewer', 'editor']:
            return True
    return False

# Files


@app.route('/api/folders/<folder_id>/files', methods=['POST'])
def post_file(folder_id):
    collection = db['folders']
    folder = collection.find_one({'_id': ObjectId(folder_id)})
    if not folder:
        return jsonify({'error': 'Folder not found'}), 404
    user_id = request.args.get('user_id')
    if not has_permission(folder, user_id, role='editor'):
        return jsonify({'error': 'Unauthorized access'}), 403
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    filename = file.filename
    s3.upload_fileobj(file, bucket_name, filename)
    files_collection = db['files']
    file_metadata = {
        'filename': filename,
        'folder_id': folder_id,
        'size': file.content_length,
        'content_type': file.content_type,
    }
    result = files_collection.insert_one(file_metadata)
    file_id = str(result.inserted_id)
    collection.update_one(
        {'_id': ObjectId(folder_id)},
        {'$push': {'files': file_id}}
    )
    return jsonify({'file_id': file_id}), 201


@app.route('/api/files/<file_id>', methods=['GET'])
def get_file(file_id):
    files_collection = db['files']
    file_metadata = files_collection.find_one({'_id': ObjectId(file_id)})
    if not file_metadata:
        return jsonify({'error': 'File not found'}), 404
    folder_id = file_metadata['folder_id']
    collection = db['folders']
    folder = collection.find_one({'_id': ObjectId(folder_id)})
    user_id = request.args.get('user_id')
    if not has_permission(folder, user_id):
        return jsonify({'error': 'Unauthorized access'}), 403
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': file_metadata['filename']},
        ExpiresIn=3600
    )
    file_metadata['_id'] = str(file_metadata['_id'])
    file_metadata['folder_id'] = str(file_metadata['folder_id'])
    return jsonify({
        'metadata': file_metadata,
        'download_url': presigned_url
    }), 200


@app.route('/api/folders/<folder_id>/files', methods=['GET'])
def get_folder_files(folder_id):
    collection = db['folders']
    folder = collection.find_one({'_id': ObjectId(folder_id)})
    if not folder:
        return jsonify({'error': 'Folder not found'}), 404

    user_id = request.headers.get('User-Id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    if not has_permission(folder, user_id):
        return jsonify({'error': 'Unauthorized access'}), 403

    files_collection = db['files']
    files = list(files_collection.find({'folder_id': folder_id}))
    for file in files:
        file['_id'] = str(file['_id'])
        file['folder_id'] = str(file['folder_id'])

    return jsonify(files), 200

# Messages


@app.route('/api/messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    collection = db['messages']
    messages = list(collection.find(
        {'$or': [{'sender_id': user_id}, {'recipient_id': user_id}]}))
    for message in messages:
        message['_id'] = str(message['_id'])
    return jsonify(messages), 200


@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    collection = db['messages']
    result = collection.insert_one(data)
    message_id = str(result.inserted_id)
    socketio.emit('new_message', {'_id': message_id,
                  **data}, room=data['recipient_id'])
    return jsonify({'_id': message_id}), 201


@app.route('/api/messages/<message_id>', methods=['PUT'])
def update_message(message_id):
    data = request.get_json()
    collection = db['messages']
    result = collection.update_one(
        {'_id': ObjectId(message_id)}, {'$set': data})
    if result.modified_count > 0:
        socketio.emit('update_message', {'_id': message_id, **data}, room)


if __name__ == '__main__':
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.run(host='0.0.0.0', port=5000, debug=True)
