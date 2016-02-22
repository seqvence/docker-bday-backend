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

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class DBdriver:

    def __init__(self, config):
        self.dbParam = config
        self.dbHandle = None
        self.cHandle = None
        self.client = None
        self.post = None

        self.connect()

    def connect(self):
        """
        Connects to Database(s) and generates handlers for Database and Collection
        :return: () -> None
        """
        try:
            self.client = MongoClient(self.dbParam['hostname'],
                                      int(self.dbParam['portNo']), serverSelectionTimeoutMS=5)
            self.client.server_info()
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        self.dbHandle = self.client[self.dbParam['database']]
        self.cHandle = self.dbHandle[self.dbParam['collection']]

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
        try:
            self.post['submissionTime'] = str(datetime.datetime.utcnow())
            self.post['status'] = "submitted"
            self.post['statusmsg'] = "Waiting for images to be tested"
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

    def get_all_records(self):
        """
        Retrieves all documents in collection
        :return: dict
        """
        return dumps(self.cHandle.find({'status': 'successful'}))

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
