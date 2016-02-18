import json

import app_config as config
from dbController import DBdriver


mongo = DBdriver(config.database)

with open('setup/sampleRecord.json') as fd:
    records = json.load(fd)

for record in records:
    mongo.insert_record(record)
