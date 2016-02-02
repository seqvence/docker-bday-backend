__author__ = 'valentinstoican'

import datetime
import json
import logging
import sys

import bson
from bson.objectid import ObjectId
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(message)s'))

class dbDriver():
    def __init__(self):
        '''
        Loads configuration file into a dictionary
        Connects to Database(s)
        :return:
        '''
        try:
            with open("config/dbConfig.json") as configFile:
                self.dbConfig = json.load(configFile)
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        self.dbParam = self.dbConfig['database1']
        self.connect()
        self.post = dict()


    def connect(self):
        '''
        Connects to Database(s) and generates handlers for Database and Collection
        :return: () -> None
        '''
        try:
            self.client= MongoClient(self.dbParam['hostname'],
                        int(self.dbParam['portNo']), serverSelectionTimeoutMS=5)
            self.client.server_info()
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        self.dbHandle = self.client[self.dbParam['database']]
        self.cHandle = self.dbHandle[self.dbParam['collection']]

        return


    def insertRecord(self,post):
        '''
        Inserts a record into the Database.
        :param post: json as string
        :return: ObjectId or None
        '''
        self.post = post
        try:
            self.post['submissionTime'] = str(datetime.datetime.utcnow())
            post_id = self.cHandle.insert_one(self.post).inserted_id
            logging.debug(post_id)
            return post_id
        except Exception,e:
            logging.error(e)
            return None

    def retrieveRecord(self,id):
        '''
        Returns corresponding record to the ObjectId passed as param
        :param id: str
        :return:
        '''
        try:
            response = self.cHandle.find_one({"_id": ObjectId(id)})
            del response['_id']
            return response
        except bson.errors.InvalidId, e:
            logging.error(e)
            return None
        except TypeError,e:
            logging.error(e)
            return None

    def disconnect(self):
        self.client.close()
        return

    def _validJson(self,data):
        try:
            logging.info(data)
            self.post = json.loads(data)
        except ValueError, e:
            logging.error(e)
            return False
        return True

def main():
    a = dbDriver()
    for i in range(1):
        subID = a.insertRecord('{"a": "a"}')
        logging.info(a.retrieveRecord(subID))
    a.disconnect()

if __name__ == '__main__':
    main()