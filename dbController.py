import json
import logging
import sys

import bson
import datetime
from bson.errors import InvalidId
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo import ReturnDocument
from pymongo import ASCENDING, DESCENDING

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class DBdriver:

    def __init__(self, config):
        self.dbParam = config
        self.dbHandle = None
        self.cHandle = None
        self.msHandle = None
        self.client = None
        self.post = None

        self.connect()

    def connect(self):
        """
        Connects to Database(s) and generates handlers for Database and Collection
        :return: () -> None
        """
        try:
            self.client = MongoClient('mongodb://' +
                                      self.dbParam['username'] + ':' +
                                      self.dbParam['password'] + '@' +
                                      self.dbParam['hostname'] + ':' +
                                      self.dbParam['portNo'] +
                                      '/?replicaSet=' +
                                      self.dbParam['replicaSet']
                                      )
            self.client.server_info()
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        self.dbHandle = self.client[self.dbParam['database']]
        self.cHandle = self.dbHandle[self.dbParam['collection']]
        self.msHandle = self.dbHandle[self.dbParam['mapStatsCollection']]

    def retrieve_record(self, db_id):
        """
        Returns corresponding record to the ObjectId passed as param
        :param db_id: str
        :return:
        """
        try:
            response = self.cHandle.find_one({"_id": ObjectId(db_id)})
            del response['_id']
            return response
        except bson.errors.InvalidId, e:
            logging.error(e)
            return None
        except TypeError, e:
            logging.error(e)
            return None

    def insert_record(self, post):
        """
        Inserts a record into the Database.
        :param post: json as string
        :return: ObjectId or None
        """
        self.post = post
        post_id = "None"
        try:
            prev_post = None
            # Check status for the last submission with the same information
            for record in self.cHandle.find(post, {'_id': 1, 'status': 1}).sort('submissionTime', DESCENDING):
                prev_post = record
                break

            self.post['status'] = "submitted"
            self.post['submissionTime'] = str(datetime.datetime.utcnow())
            self.post['statusmsg'] = "Waiting for images to be tested"

            if prev_post is not None:
                # if status is in the list "successful", "submitted", "pending", "duplicated"
                # return id
                if prev_post['status'] in ("successful", "submitted", "pending", "duplicated"):
                    logging.debug("Previous submission is being processed or has already been processed.")
                    return str(prev_post['_id'])
                # If status is failed new record is inserted
                elif prev_post['status'] == "failed":
                    logging.debug("Previous submission failed. Let's try it again!")
                    post_id = self.cHandle.insert_one(self.post).inserted_id
                # Change status to submitted
                else:
                    logging.debug("Unknown status. Status changed to submitted")
                    self.update_record_status(id=prev_post["_id"], status="submitted")
                    post_id = str(prev_post["_id"])
            # if no previous record a new record is inserted
            else:
                post_id = self.cHandle.insert_one(self.post).inserted_id
            logging.debug(post_id)
            return post_id
        except Exception, e:
            logging.error(e)
            return None

    def get_one_record(self):
        """
        Retrieve one record with status "submitted" and updates the status to "pending"
        :return: dict
        """
        return self.cHandle.find_one_and_update({'status': 'submitted'}, {'$set': {'status': 'pending'}},
                                                return_document=ReturnDocument.AFTER)

    def get_all_records(self, status):
        """
        Retrieves all documents in collection
        :param status: string
        :return: dict
        """
        response = dict()
        response['submissions'] = list(self.cHandle.find(filter={'status': status},
                                       projection={'_id': True,
                                                   'name': True,
                                                   'twitter': True,
                                                   'coordinates': True}))
        for record in response['submissions']:
            record['id'] = str(record['_id'])
            del record['_id']

        response['votes_stats'] = self.cHandle.group(key={'vote': 1},
                                                     condition={'status': status},
                                                     initial={"count": 0},
                                                     reduce="function(o, p) {p.count++}")

        response['votes'] = dict()

        for record in response['votes_stats']:
            response['votes'][record['vote'].title()] = int(record['count'])

        del response['votes_stats']

        return dumps(response)

    def get_successful_stats(self):
        try:
            return dumps(json.loads(self.msHandle.find({}, {"_id": 0, "name": 0})[0]))
        except Exception, e:
            logging.error(e)
            return self.get_all_records(status="successful")

    def update_record_status(self, id, status):
        """
        Update submission status
        :param id: Object(id)
        :param status: string
        :return: None
        """
        post = {
            "$set": {
                "status": status
            }
        }
        self.cHandle.update({"_id": id}, post)

        return

    def disconnect(self):
        """
        Disconnect from database
        :return: None
        """
        self.client.close()
        return

    def _valid_json(self, data):
        """
        Convert data to json. Returns True or False whether the input is a valid JSON format or not
        :param data:
        :return: boolean
        """
        try:
            logging.info(data)
            self.post = json.loads(data)
        except ValueError, e:
            logging.error(e)
            return False
        return True
