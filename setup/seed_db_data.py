import json

import app_config as config
from db.controller import dbDriver


mongo = dbDriver(config.database)

with open('setup/sampleRecord.json') as fd:
    records = json.load(fd)

for record in records:
    mongo.insertRecord(record)