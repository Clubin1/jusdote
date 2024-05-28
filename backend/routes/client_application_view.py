from flask.views import MethodView
from db import db

class ClientApplicationView(MethodView):
    def __init__(self):
        self.collection = db['client_applications']
    
    def get(self, id=None):
        if id is None:
            applications = list(self.collection.find())
            for app in applications:
                app['_id'] = str(app['_id'])
                return jsonify(applications), 200
        else:
            application = self.collection.find_one({'_id': ObjectId(id)})
            if application:
                application['_id'] = str(application['_id'])
                return jsonify(application), 200
            else:
                return jsonify({'error': 'Application not found'}), 404

    def post(self):
        data = request.get_json()
        result = self.collection.insert_one(data)
        application_id = str(result.inserted_id)
        return jsonify({'_id': application_id}), 201

    def put(self, id):
        data = request.get_json()
        result = self.collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count > 0:
            return jsonify({'message': 'Application updated successfully'}), 200
        else:
            return jsonify({'error': 'Application not found'}), 404

    def delete(self, id):
        result = self.collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Application deleted successfully'}), 200
        else:
            return jsonify({'error': 'Application not found'}), 404