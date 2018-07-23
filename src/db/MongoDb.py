#! /usr/bin/python3
# _*_ coding:utf-8 _*_
import logging

import yaml
from pymongo import MongoClient


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
        logging.debug('Begin to connect mongodb.')
        self.uri = 'mongodb://' + self.mongodb_user + ':' + self.mongodb_password + '@' + self.mongodb_address + '/'+ self.mongodb_dbname
        self.client = MongoClient(self.uri)
        self.mongodb = self.client[self.mongodb_dbname]
        self.mongodb_collection = self.mongodb.get_collection(self.mongo_collection)
        logging.debug('Connecting mongodb successfully.')

    def get_time_span_data(self, date_str_list, chunk_size):
        data_list = []
        cache_record = []
        for date in date_str_list:
            cursor = self.mongodb_collection.find({'slot.owner.from': {'$regex': date}})
            for i, record in enumerate(cursor):
                cache_record.append(record)
                if i % chunk_size == chunk_size - 1:
                    data_list = data_list + cache_record
                    cache_record = []
            if cache_record:
                data_list = data_list + cache_record
                cache_record = []
        return data_list
