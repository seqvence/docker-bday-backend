import json
import time

from flask import Flask, request
from flask_restful import Resource, Api

import app_config as config
import validateSubmission
from dbController import DBdriver

time.sleep(3)

app = Flask(__name__, static_folder='static')
api = Api(app)

mongo = DBdriver(config.database)


class StaticAssets(Resource):
    @classmethod
    def get(self, path):
        """
        Returns resource from static directory
        :param path:
        :return: get(str) -> file
        """
        return app.send_static_file(path)


class Index(Resource):
    @classmethod
    def get(self):
        """
        Returns index from static directory
        :return: get() -> file
        """
        return app.send_static_file('index.html')


class RetrieveStatus(Resource):
    @classmethod
    def get(self, submission_id):
        """
        Check the database for the status of the submission with the id submission_id
        :param submission_id:
        :return: get(int) -> str
        """
        return {'response': mongo.retrieve_record(submission_id)}, 200


class Submission(Resource):
    def post(self):
        """
        Accepts post requests and store them in the database.
        :return: post(json) -> json, http_code
        """
        check_input = validateSubmission.validate_input(request.json)
        if check_input[0]:
            submission_id = mongo.insert_record(request.json)
            return {'response': "Congratulations for your submission. Your id is: {}".format(str(submission_id))}, 200
        else:
            return {'response': "Your submission was not successfful due to: {}".format(check_input[1])}, 200


class Stats(Resource):
    @classmethod
    def get(self):
        records = mongo.get_all_records()
        return json.loads(records), 200


# Static assets
api.add_resource(StaticAssets, '/<path:path>')
api.add_resource(Index, '/')

# Create /competition endpoint
api.add_resource(Submission, '/competition')

# Create /competition/<int:submissionID> endpoint
api.add_resource(RetrieveStatus, '/competition/<string:submissionID>')

# Create /stats endpoint
api.add_resource(Stats, '/stats')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
