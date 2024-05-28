from flask import Flask
from routes.editor_application_view import EditorApplicationView
from routes.client_application_view import ClientApplicationView
from db import client
from routes.message_view import MessageView, socketio
from routes.auth_view import SignupView, LoginView, ProtectedView, bcrypt, jwt
from routes.folder_view import Folder

app = Flask(__name__)
socketio.init_app(app)
app.config['JWT_SECRET_KEY'] = 'u0GJPnC7BX89TXoykxo3D7zR7rdORWXGkhR7kxuToHI='
bcrypt.init_app(app)
jwt.init_app(app)

def check_mongodb_connection():
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"MongoDB connection error: {e}")

@app.route('/')
def home():
    return 'Hello, World!'

app.add_url_rule('/api/editor/applications', view_func=EditorApplicationView.as_view('editor_applications'))
app.add_url_rule('/api/editor/applications/<id>', view_func=EditorApplicationView.as_view('editor_application'))
app.add_url_rule('/api/client/applications', view_func=ClientApplicationView.as_view('client_applications'))
app.add_url_rule('/api/client/applications/<id>', view_func=ClientApplicationView.as_view('client_application'))
app.add_url_rule('/api/messages', view_func=MessageView.as_view('messages'))
app.add_url_rule('/api/messages/<id>', view_func=MessageView.as_view('message'))
app.add_url_rule('/api/folders', view_func=Folder.as_view('create_folder'), methods=['POST'])
app.add_url_rule('/api/folders', view_func=Folder.as_view('get_user_folders'), methods=['GET'])
app.add_url_rule('/api/folders/<folder_id>', view_func=Folder.as_view('get_single_folder'), methods=['GET'])
app.add_url_rule('/signup', view_func=SignupView.as_view('signup'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/protected', view_func=ProtectedView.as_view('protected'))

if __name__ == '__main__':
    check_mongodb_connection()
    socketio.run(app, debug=True)
    app.run(debug=True)