import logging
import re
import urllib

import requests
from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import StringType, BaseType
from schematics.types.compound import ListType

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)-15s() %(levelname)s %(message)s')


def validate_input(input_data):
    """
    Check submission data against a datamodel and returns boolean and error message.
    :rtype: string
    :param input_data
    :return: boolean, string
    """
    try:
        Submission(input_data).validate()
        for value in input_data.values():
            if _profanity_check(str(value)):
                return False, "Value /{}/ not accepted.".format(value)
        return True, ""
    except Exception, e:
        logging.error(e)
        return False, e


def _profanity_check(data):
    """
    Performs profanity checks
    :param data: string
    :return: boolean
    """
    try:
        response = requests.get("http://www.wdyl.com/profanity?q=" + urllib.pathname2url(data), timeout=1)
        if "true" in response.text:
            return True
        else:
            return False
    except Exception, e:
        logging.error("Failed to perform profanity check due to {}.".format(e))
        return False


class Twitter(BaseType):
    def to_primitive(self, value, context=None):
        if value is not None:
            return u'{0}'.format(value)

    def validate_twitter(self, value):
        if value is not None:
            if not re.match('^@([A-Za-z0-9_]+)$', value) or not len(value) > 2:
                raise ValidationError("Value must be valid Twitter acount of the form @username")


class Submission(Model):
    name = StringType(required=True, min_length=5, max_length=50)
    twitter = Twitter()
    location = StringType(required=True, min_length=1, max_length=100)
    repo = ListType(StringType(required=True, regex="^[a-zA-Z0-9-_/:.]*$"), required=True)
    vote = StringType(required=True, min_length=1, max_length=50)
