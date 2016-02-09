__author__ = 'valentinstoican'

import logging
import threading
from time import sleep

import click

from dbController import dbDriver

endpoint = "http://localhost:5000/competition/"

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(message)s'))

@click.command()
@click.option('--submissions', default=10, type=click.IntRange(1, 20), help='Number of submissions to be processed per minute [1-20]')
def dockerWorker(submissions):
    threading.Timer(float(60/submissions), dockerWorker).start()
    mongo = dbDriver()
    sleep(6)
    record = mongo.getOneRecord()
    if record is None:
        logging.info("Idle.")
    else:
        logging.info(record)

def testEndpoint():
    pass

if __name__ == '__main__':
    dockerWorker()





