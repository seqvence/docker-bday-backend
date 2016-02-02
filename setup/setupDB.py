__author__ = 'valentinstoican'

import json
import logging
import sys

from pymongo import MongoClient

configFile = "DB.config"
sampleRecordFile = "sampleRecord.json"
logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(message)s'))

def checkDB(**data):
    '''

    :param hostname:
    :param portNo:
    :param collection:
    :return:
    '''
    client=dict()
    logging.info("Checking DB availability.")
    try:
        logging.debug("Trying to connect to %s DB %s on port %s" % (data['role'], data['hostname'], data['portNo']))
        client[data['role']] = MongoClient(data['hostname'], int(data['portNo']))
        logging.debug(client[data['role']].database_names())
        if client[data['role']].connect:
            logging.debug("Successfully connected.")
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    logging.info("Checking database %s DB %s on port %s for ReplicaSet configured." % (data['role'], data['hostname'], data['portNo']))
    try:
        logging.info(client[data['role']].admin.command("rs.stats()"))
    except Exception as e:
        logging.error(e)
        sys.exit(1)


    logging.debug("Closing connection to %s DB %s." % (data['role'], data['hostname']))
    client[data['role']].close()
    logging.info("%s database (%s:%s) is online." % ((data['role']).title(), data['hostname'], data['portNo']))

def enableReplicaSet(**data):

    return True

def main():
    try:
        with open(configFile) as config_file:
            config = json.load(config_file)
    except Exception as e:
        logging.error("Loading configuration failed due to: %s" % (e))
        sys.exit(e.errno)

    for key, values in config.items():
        checkDB(**values)





#    if data['role'] == 'primary':
#        try:
#            logging.info("Loading sample record into the %s DB" % data['role'])
#            with open(sampleRecordFile) as sRecord:
#                sampleRecord = json.load(sRecord)
#            #sampleRecord['submissionTime'] =
#            logging.info(sampleRecord)
#            client[data['role']].db[data['collection']]
#        except Exception as e:
#            logging.error(e)
#            sys.exit(1)




if __name__ == '__main__':
    main()
