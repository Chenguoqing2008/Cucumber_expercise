#! /usr/bin/python

import logging
import yaml
from pandas.io.json import json_normalize
import time
from db.MySql import MySql
from db.MongoDb import MongoDb
from Util.DateInfo import DateInfo
from Util.DataFrameFactory import DataFrameFactory


class MongoToPandas:

    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    chunk_size = 5
    config = yaml.load(open("comparison_config.yaml"))
    unused_columns = ['_id', 'eid', '_class', 'from', 'to', 'summary', 'location', 'slot._id', 'slot.repeat',
                      'slot.owner.slotId', 'slot.owner.from', 'slot.owner.to', 'slot.owner.name', 'slot.owner.username',
                      'slot.updatedAt', 'slot.createdAt', 'slot.owner.phone']

    def __init__(self, mongodb, mysql):
        self.mongodb = mongodb
        self.mysql = mysql
        self.storeid_list = self.mysql.get_storeid()
        logging.debug("Storeid list is %s", self.storeid_list)

    def generate_dataframe_rawdata(self, start_date_str, end_date_str):
        start_date = DateInfo.get_date_week_begin(start_date_str)
        end_date = DateInfo.get_date_week_end(end_date_str)
        date_str_list = DateInfo.get_date_string_list(start_date, end_date)
        raw_data = self.mongodb.get_time_span_data(date_str_list, self.chunk_size)
        logging.debug("raw data list is %s", len(raw_data))
        return raw_data

    def get_base_dataframe(self, raw_data):
        schedule_df = json_normalize(raw_data)
        logging.debug('Total columns is %s', schedule_df.shape[0])
        schedule_df = schedule_df.drop(columns=self.unused_columns)
        return schedule_df


def main():

    begin_time = time.time()
    mongodb = MongoDb()
    mysql = MySql()
    mongotopandas = MongoToPandas(mongodb, mysql)

    begin_time2 = time.time()
    start_time = '2018-07-10'
    end_time = '2018-07-10'
    rawdata_list = mongotopandas.generate_dataframe_rawdata(start_time, end_time)
    dataframe_base = mongotopandas.get_base_dataframe(rawdata_list)
    print(dataframe_base.head())
    end_time2 = time.time()
    load_time = end_time2 - begin_time2
    logging.debug('Loading pandas spend time %s', load_time)
    dataframe_factory = DataFrameFactory(dataframe_base)
    dataframe1 = dataframe_factory.filter_storeid(mongotopandas.storeid_list)\
                                  .dataframe_convert_datetime()\
                                  .add_title_state_weekday_column()

    # dataframe2 = mongotopandas.add_title_state_weekday_column(dataframe)
    print(dataframe1.dataframe.head())
    end_time = time.time()
    time_span = end_time - begin_time
    logging.debug('Convert date time type taken %s', time_span)


if __name__ == '__main__':
    main()





