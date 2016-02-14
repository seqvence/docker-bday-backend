import app_config as config
from dbController import dbDriver

import logging
from docker import Client
import click

logging.basicConfig(format=('%(asctime)s %(levelname)s %(message)s'), level=logging.DEBUG, )

#@click.command()
#@click.option('--submissions', default=10, type=click.IntRange(1, 20), help='Number of submissions to be processed per minute [1-20]')
def docker_worker():
    mongo = dbDriver(config.database)
    record = mongo.getOneRecord()
    if not record:
        logging.info("Idle.")
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
    return True


def run_container(image):
    cli = Client(base_url=config.docker['api'])
    container = cli.create_container(image=image, command='/bin/sleep 60')
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




