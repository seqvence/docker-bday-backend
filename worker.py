import eventlet

eventlet.monkey_patch()  # NOQA

import app_config as config
from dbController import dbDriver

from docker import Client
import logging
import requests
import click

logging.basicConfig(format=('%(asctime)s %(levelname)s %(message)s'), level=logging.DEBUG, )

@click.command()
@click.option('--submissions', default=5, help='Number of submissions to be processed per interval (Default: 5)')
@click.option('--interval', default=30, help='Interval used to process new submissions Default: 30)')
def docker_worker(submissions, interval):
    pool = eventlet.GreenPool(size=100)

    while True:
        try:
            for _ in xrange(submissions):
                pool.spawn(check_submission)
            logging.info('Waiting for {} seconds'.format(interval))
            eventlet.sleep(interval)
        except (SystemExit, KeyboardInterrupt):
            break


def check_submission():
    mongo = dbDriver(config.database)
    record = mongo.getOneRecord()
    if not record:
        logging.info("Quiting. No new submission.")
        return
    logging.info('Starting container {} for user {}'.format(record['repo'][0], record['name']))
    test_result = run_container(record['repo'][0])
    logging.info('Updating submission status for {}'.format(record['name']))
    if test_result:
        mongo.update_record_status(record['_id'], 'successful')
    else:
        mongo.update_record_status(record['_id'], 'failed')


def test_endpoint(ip, port):
    logging.info('Testing endpoing {}:{}'.format(ip, port))
    try:
        r = requests.get('http://{}:{}'.format(ip, port), timeout=3)
    except requests.exceptions.Timeout:
        return False
    if r.status_code == 200:
        return True
    else:
        return False


def run_container(image):
    cli = Client(base_url=config.docker['api'])
    container = cli.create_container(image=image)
    cli.start(container=container.get('Id'))
    container = cli.inspect_container(container=container.get('Id'))
    if container['State']['Status'] != 'running':
        logging.error('Container {} died too soon.'.format(image))
        return
    if not container['NetworkSettings']['IPAddress']:
        logging.error('Container {} has no network. Something went wrong'.format(image))
        return
    test_result = test_endpoint(container['NetworkSettings']['IPAddress'], 80)
    logging.info('Stoping container {}'.format(image))
    cli.stop(container=container.get('Id'), timeout=20)
    return test_result

if __name__ == '__main__':
    docker_worker()



