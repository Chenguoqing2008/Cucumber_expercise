#! /usr/bin/python3
# _*_ coding:utf-8 _*_
import logging
import yaml
from pymongo import MongoClient
import bson


class MongoDb:
    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    config = yaml.load(open("comparison_config.yaml"))

    logging.debug('Start to connect mongodb.')
    mongodb_host = config['mongodb']['ip']
    mongodb_port = config['mongodb']['port']
    mongodb_user = config['mongodb']['username']
    mongodb_password = config['mongodb']['password']
    mongodb_dbname = config['mongodb']['dbname']
    mongo_collection = config['mongodb']['collection']
    mongodb_address = mongodb_host + ':' + str(mongodb_port)

    def __init__(self):
        uri = 'mongodb://' + self.mongodb_user + ':' + self.mongodb_password + '@' + self.mongodb_address + '/'+ self.mongodb_dbname
        client = MongoClient(uri)
        mongodb = client[self.mongodb_dbname]
        self.mongodb_collection = mongodb.get_collection(self.mongo_collection)
        logging.debug('Connecting mongodb successfully.')

    def get_mongodb_type(self, storeid, uid, date):
        collection = self.mongodb_collection
        schedule_record = collection.find({'storeId': storeid,
                                           'slot.owner.uid': uid, 'slot.date': {'$regex': date}})
        logging.debug(
            "Mongodb query with internal storeid: %d uid: %d date: %s is processing. ",
            storeid, uid, date)
        if schedule_record.count() > 2:
            logging.debug('Retrieving storeId, uid, date in mongodb don\'t get unique result.')
            return 'Query mongodb parameters are wrong.'
        if schedule_record.count() == 0:
            logging.debug("Querying mongodb result is not in 'SCHEDULE', "
                          "'AVAILABILITY', 'UNAVAILABLE', 'REQUEST', 'DAYOFF'")
            return None
        else:
            for doc in schedule_record:
                schedule_data = bson.BSON.encode(doc)
                decoded_schedule_data = bson.BSON.decode(schedule_data)
                for key, value in decoded_schedule_data.items():
                    if key == 'slot':
                        for slot_key, slot_value in value.items():
                            if slot_key == 'type':
                                return slot_value
