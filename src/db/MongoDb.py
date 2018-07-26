#! /usr/bin/python3
# _*_ coding:utf-8 _*_
import logging
import yaml
from pymongo import MongoClient
from multiprocessing import Queue
import threading

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

uri = 'mongodb://' + mongodb_user + ':' + mongodb_password + '@' \
           + mongodb_address + '/' + mongodb_dbname
client = MongoClient(uri)
mongodb = client[mongodb_dbname]
mongodb_collection = mongodb.get_collection(mongo_collection)

data_queue = Queue()


class MongoDb(threading.Thread):
    def __init__(self, date_str, name):
        threading.Thread.__init__(self)
        self.date_str = date_str
        self.name = name

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

    def run(self):
        logging.debug('Start thread %s', self.name)
        get_certain_date_data(self.date_str)


def get_certain_date_data(date_str):
    cursor = mongodb_collection.find({'slot.owner.from': {'$regex': date_str}})
    for i, record in enumerate(cursor):
        data_queue.put(record)


def run_mongo_converter(date_str_list):
    threads = []
    for date in date_str_list:
        process_thread = MongoDb(date, 'Thread-'+date)
        threads.append(process_thread)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    logging.debug("Generate mongodb data to queue successfully.")
    return data_queue



