__author__ = 'valentinstoican'

import json
import unittest
from unittest import TestCase

from requests import post, get

webserverIP = 'localhost'
webserverPort = '5000'

class TestSubmission(TestCase):
    def test_post(self):
        '''
        Test for a POST request to return a json response
        :return:
        '''
        url = 'http://' + webserverIP + ':' + webserverPort +'/competition'
        headers = {'content-type': 'application/json'}
        message ={
            "name": "Mano Marks",\
            "twitter-handle": "@ManoMarks",\
            "location": "San Francisco, CA, USA",\
            "test": "test",\
            "repo": ["manomarks/docker-birthday-1", "manomarks/docker-birthday-2", "manomarks/docker-birthday-3"],\
            "vote": "node.js"\
        }
        response = post(url, data=json.dumps(message), headers=headers)
        try:
            json.dumps(response.content)
        except:
            self.fail()

    def test_get(self):
        '''
        Test for GET request not to be allowed on this endpoint
        :return: None
        '''
        self.assertTrue("405" in str(get('http://' + webserverIP + ':' + webserverPort +'/competition')))


if __name__ == '__main__':
    unittest.main()