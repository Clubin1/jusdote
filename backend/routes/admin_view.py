from flask import request, jsonify
from flask.views import MethodView
from db import db

class AdminView(MethodView):
    def __init__(self) -> None:
        self.collection = db['admins']

    