__author__ = 'valentinstoican'

import unittest
from unittest import TestCase
from requests import post, get
import json


class TestSubmission(TestCase):
    def test_post(self):
        '''
        Test for a POST request to return a json response
        :return:
        '''
        message = post('http://localhost:5000/competition',
                       data={
                           "name": "Mano Marks", \
                           "twitter-handle": "@ManoMarks", \
                           "location": "San Francisco, CA, USA", \
                           "repo": ["manomarks/docker-birthday-1", "manomarks/docker-birthday-2",
                                    "manomarks/docker-birthday-3"], \
                           "vote": "node.js"
                       }
        ).json()
        try:
            json.dumps(message)
        except:
            self.fail()

    def test_get(self):
        '''
        Test for GET request not to be allowed on this endpoint
        :return: None
        '''
        self.assertTrue("405" in str(get('http://localhost:5000/competition')))


if __name__ == '__main__':
    unittest.main()