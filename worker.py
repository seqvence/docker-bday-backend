__author__ = 'valentinstoican'

import logging
import threading

import click

from dbController import dbDriver

endpoint = "http://localhost:5000/competition/"

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(message)s'))

@click.command()
@click.option('--submissions', default=10, help='Number of submissions to be processed per minute [1-20]')
def dockerWorker(submissions):
    threading.Timer(float(60/submissions), dockerWorker).start()
    mongo = dbDriver()
    record = mongo.getOneRecord()
    if record is None:
        logging.info("Idle.")
    else:
        logging.info(record)

def testEndpoint():
    pass

if __name__ == '__main__':
    dockerWorker()





