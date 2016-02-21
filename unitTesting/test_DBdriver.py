from unittest import TestCase
from dbController import DBdriver
import app_config as config


class TestDBdriver(TestCase):
    def test_connect(self):
        dbdriver = DBdriver(config.database)
        dbdriver.connect()
        self.assertIsNotNone(dbdriver.dbHandle)
        self.assertIsNotNone(dbdriver.cHandle)
        dbdriver.disconnect()

    def test_insert_record(self):
        dbdriver = DBdriver(config.database)
        dbdriver.connect()
        object_id = dbdriver.cHandle.insert_one({"dummyRecord": "dummyRecord"}).inserted_id
        self.assertIsNotNone(object_id)
        dbdriver.cHandle.remove({"_id": object_id})
        dbdriver.disconnect()

    def test_get_one_record(self):
        dbdriver = DBdriver(config.database)
        dbdriver.connect()

        document = dbdriver.get_one_record()
        if document is None:
            object_id = dbdriver.cHandle.insert_one({"status": "submitted"}).inserted_id
            document = dbdriver.get_one_record()
            self.failUnlessEqual(str(object_id), str(document["_id"]))
            dbdriver.cHandle.remove({"_id": object_id})
        else:
            self.assertEqual(document['status'], "pending")

        dbdriver.cHandle.remove({"_id": document["_id"]})
        dbdriver.disconnect()

    def test_get_all_records(self):
        dbdriver = DBdriver(config.database)
        dbdriver.connect()

        document = dbdriver.get_all_records()
        if len(document) == 2:
            object_id = dbdriver.cHandle.insert_one({"status": "successful"}).inserted_id
            document = dbdriver.get_all_records()
            self.assertIsNotNone(document)
            dbdriver.cHandle.remove({"_id": object_id})
        self.assertGreater(len(document), 2)

        dbdriver.disconnect()

    def test_update_record_status(self):
        dbdriver = DBdriver(config.database)
        dbdriver.connect()

        object_id = dbdriver.cHandle.insert_one({"status": "dummyrecord"}).inserted_id
        dbdriver.update_record_status(object_id, "test_dummyrecord")
        self.assertEquals(len(dbdriver.cHandle.find_one({"status": "test_dummyrecord"})), 2)
        dbdriver.cHandle.remove({"_id": object_id})

        dbdriver.disconnect()

    def test__valid_json(self):
        dbdriver = DBdriver(config.database)
        self.assertFalse(dbdriver._valid_json('{"Invalid : "test"}'))

