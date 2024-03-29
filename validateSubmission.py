import logging
import re
import urllib

import requests
from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import StringType, BaseType
from schematics.types.compound import ListType
from profanityChecker import ProfanityChecker

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)-15s() %(levelname)s %(message)s')


def validate_input(input_data):
    """
    Check submission data against a datamodel and returns boolean and error message.
    :rtype: string
    :param input_data
    :return: boolean, string
    """
    p_checker = ProfanityChecker()
    try:
        Submission(input_data).validate()
        for value in input_data.values():
            if p_checker.validate(str(value)):
                return False, "Value /{}/ not accepted in {}.".format(p_checker.validate(str(value)), value)
        return True, ""
    except Exception, e:
        logging.error(e)
        return False, e


class Twitter(BaseType):
    def to_primitive(self, value, context=None):
        if value is not None:
            return u'{0}'.format(value)

    def validate_twitter(self, value):
        if value is not None:
            if not re.match('^@([A-Za-z0-9_]+)$', value) or not len(value) > 2:
                raise ValidationError("Value must be valid Twitter account of the form @username")


class Submission(Model):
    name = StringType(required=True, min_length=3, max_length=50)
    twitter = Twitter()
    location = StringType(required=True, min_length=1, max_length=100)
    repo = ListType(StringType(required=True, regex="^[a-zA-Z0-9-_/:.]*$"), min_size=1, max_size=3, required=True)
    vote = StringType(required=True, min_length=1, max_length=50)
