__author__ = 'valentinstoican'

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

submissions = {}


class RetrieveStatus(Resource):
    def get(self, submissionID):
        '''
        Check the database for the status of the submission with the id submissionID
        :param submissionID:
        :return: get(int) -> str
        '''
        if submissionID in submissions:
            return jsonify(message='SubmissionID %i found' % submissionID)
        else:
            return jsonify(message='SubmissionID %i not found' % submissionID)


class Submission(Resource):
    def post(self):
        '''
        Accepts post requests and store them in the database
        :return: post(json) -> json, http_code
        '''
        submissionID = len(submissions) + 1
        submissions[submissionID] = request.form['name']
        return {'response': 'Congratulations for your submission. Your id is:' + str(submissionID)}, 200


class Stats(Resource):
    def get(self):
        return None, 200

# Create /competition endpoint
api.add_resource(Submission, '/competition')

# Create /competition/<int:submissionID> endpoint
api.add_resource(RetrieveStatus, '/competition/<int:submissionID>')

# Create /stats endpoint
api.add_resource(Stats, '/stats')

if __name__ == '__main__':
    app.run(debug=True)











