__author__ = 'valentinstoican'

import unittest
from unittest import TestCase

webserverIP = 'localhost'
webserverPort = '5000'

class TestRetrieveStatus(TestCase):
    def test_get(self):
        self.assertIsNone('http://' + webserverIP + ':' + webserverPort +'/competition/' + '1234567')
        self.assertIsNone('http://' + webserverIP + ':' + webserverPort +'/competition/' + '9876543')

if __name__ == '__main__':
    unittest.main()