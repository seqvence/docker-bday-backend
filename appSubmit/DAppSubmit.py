__author__ = 'valentinstoican'

import json
import logging
import re

import click
import requests
import sys
from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import StringType, URLType, BaseType
from schematics.types.compound import ListType

logging.basicConfig(level=logging.INFO, format=('%(asctime)s %(levelname)s %(message)s'))

@click.command()
@click.option('--endpoint', '-e',  prompt=True, help='Webservice address to submit your information. e.g.: http://api.competition.docker.com')
@click.option('--name', '-n', prompt=True, help='Your full name. e.g.: Docker Fan')
@click.option('--twitter', '-t', default="",help='Your Twitter account. e.g: #dockerFan')
@click.option('--location', '-l', prompt=True, help='Your location e.g.: City, State, Country')
@click.option('--repo', '-r', prompt=True, help="Provide the repository(ies) for the app images. e.g:\n-r DockerImage1\n-r\nDockerImage2 etc.", multiple=True)
@click.option('--vote', '-p', prompt=True, help='Programming language used by you.')
@click.help_option()
def DAppSubmit(endpoint, name, twitter, location, repo, vote):
    inputData = Submission()
    inputData['name'] = name
    inputData['twitter'] = twitter
    inputData['location'] = location
    inputData['repo'] = repo
    inputData['vote'] = vote
    inputData['endpoint'] = endpoint

    try:
        logging.info("Validating input information.")
        inputData.validate()
        postRequest = dict(inputData)
        del(postRequest['endpoint'])
    except Exception,e:
        logging.error("Validation failed %s" % e.messages)
        sys.exit(1)

    try:
        logging.info("Sending your request")
        postHeaders={'content-type': 'application/json'}
        application = requests.post(endpoint.lower(), headers=postHeaders, data=json.dumps(postRequest))
        logging.info(json.loads(application.text)['response'])
    except Exception, e:
        logging.error(e)
        sys.exit(1)

class Twitter(BaseType):
    def to_primitive(self, value, context=None):
        if value is not None:
            return u'{0}'.format(value)
    def validate_twitter(self, value):
        if value is not None:
            if not re.match('^@([A-Za-z0-9_]+)$', value) and not len(value) > 2:
                raise ValidationError("Value must be valid Twitter acount of the form @username")


class Submission(Model):
    name = StringType(required=True, regex='^[^\W_]+(-[^\W_]+)?$', min_length=5, max_length=50)
    twitter = Twitter()
    location = StringType(required=True, min_length=1, max_length=100)
    repo = ListType(StringType(required=True, regex="^[a-zA-Z0-9/]*$"), required=True)
    vote = StringType(required=True, min_length=1, max_length=50)
    endpoint = URLType(required=True, min_length=7, max_length=50)


if __name__ == '__main__':
    DAppSubmit()
