#! /usr/bin/python
# _*_ coding:utf-8 _*_

import logging
import yaml
from pandas.io.json import json_normalize
import time
from util.DateInfo import DateInfo
from util.DataFrameFactory import DataFrameFactory
from db.MongoDb import run_mongo_converter


class MongoToPandas:
    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    config = yaml.load(open("comparison_config.yaml"))
    unused_columns = ['_id', 'eid', '_class', 'from', 'to', 'summary', 'location', 'slot._id', 'slot.repeat',
                      'slot.owner.slotId', 'slot.owner.from', 'slot.owner.to', 'slot.owner.name', 'slot.owner.username',
                      'slot.updatedAt', 'slot.createdAt', 'slot.owner.phone']

    def __init__(self):
        pass

    @staticmethod
    def generate_date_list(start_date_str, end_date_str):
        start_date = DateInfo.get_date_week_begin(start_date_str)
        end_date = DateInfo.get_date_week_end(end_date_str)
        date_str_list = DateInfo.get_date_string_list(start_date, end_date)
        return date_str_list

    def get_base_dataframe(self, queue_data):
        dataframe_list = [queue_data.get() for i in range(queue_data.qsize())]
        schedule_df = json_normalize(dataframe_list)
        logging.debug('Total columns is %s', schedule_df.shape[0])
        schedule_df = schedule_df.drop(columns=self.unused_columns)
        return schedule_df


def main():
    start_time = '2018-07-10'
    end_time = '2018-07-10'

    begin_time = time.time()
    mongotopandas = MongoToPandas()
    date_str_list = mongotopandas.generate_date_list(start_time, end_time)
    output_queue = run_mongo_converter(date_str_list)
    dataframe_base = mongotopandas.get_base_dataframe(output_queue)
    shedule_dataframe = DataFrameFactory(dataframe_base)\
        .filter_storeid()\
        .dataframe_convert_datetime()\
        .add_title_column()\
        .add_state_column()\
        .add_weekday_column().dataframe
    print(shedule_dataframe.shape)
    print(shedule_dataframe.loc[:, 'slot.from'])
    end_time = time.time()
    time_span = end_time - begin_time
    logging.debug('Convert mongodb to pandas time taken %s', time_span)


if __name__ == '__main__':
    main()





