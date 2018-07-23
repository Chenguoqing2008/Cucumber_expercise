#! /usr/bin/python

import pandas as pd
import logging
import yaml
from pandas.io.json import json_normalize
import datetime
import time
from db.MySql import MySql
from db.MongoDb import MongoDb


class MongoToPandas:

    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    chunk_size = 5
    config = yaml.load(open("comparison_config.yaml"))
    unused_columns = ['_id', 'eid', '_class', 'from', 'to', 'summary', 'location', 'slot._id', 'slot.repeat',
                      'slot.owner.slotId', 'slot.owner.from', 'slot.owner.to', 'slot.owner.name', 'slot.owner.username',
                      'slot.updatedAt', 'slot.createdAt', 'slot.owner.phone']
    uid_position_cache = {}

    def __init__(self):
        self.mongodb = MongoDb()
        self.mysql = MySql()
        begin_time2 = time.time()
        logging.debug('Loading mongodb data, this may take 1 minute.')

        end_time2 = time.time()
        time_elapse = end_time2 - begin_time2

        logging.debug("loading mongodb spend %s", time_elapse)
        logging.debug('Mapping mongodb to dataframe successfully.')
        self.storeid_list = self.mysql.get_storeid()
        logging.debug("Storeid list is %s", self.storeid_list)

    def generate_dataframe(self, start_date_str, end_date_str):
        start_date = self.get_date_week_begin(start_date_str)
        end_date = self.get_date_week_end(end_date_str)
        date_str_list = self.get_date_string_list(start_date, end_date)
        raw_data = self.mongodb.get_time_span_data(date_str_list, self.chunk_size)
        logging.debug("raw data is %s", len(raw_data))
        return raw_data

    def get_base_dataframe(self, raw_data):
        schedule_df = json_normalize(raw_data)
        logging.debug('Total columns is %s', schedule_df.shape[0])
        schedule_df = schedule_df.drop(columns=self.unused_columns)
        return schedule_df

    @staticmethod
    def get_date_week_begin(date_str):
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        calendar = date.isocalendar()
        year = calendar[0]
        week_index = int(calendar[1]) - 1
        weekday = 0

        week_string = str(year) + '-' + str(week_index) + '-' + str(weekday)
        week_start_time = datetime.datetime.strptime(week_string, '%Y-%W-%w').date()
        week_start_string = week_start_time.strftime('%Y-%m-%d')
        logging.debug('Schedule start time is %s', week_start_string)
        return week_start_string

    @staticmethod
    def get_date_string_list(start_date, end_date):
        date_list = []
        start_time = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        for index in range((end_time - start_time).days + 1):
            time_index = start_time + datetime.timedelta(days=index)
            date_list.append(datetime.datetime.strftime(time_index, '%Y-%m-%d'))
        return date_list

    @staticmethod
    def get_date_week_end(date_str):
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        calendar = date.isocalendar()
        year = calendar[0]
        week_index = int(calendar[1])
        weekday = 6

        week_string = str(year) + '-' + str(week_index) + '-' + str(weekday)
        week_end_time = datetime.datetime.strptime(week_string, '%Y-%W-%w').date()
        week_end_string = week_end_time.strftime('%Y-%m-%d')
        logging.debug('Schedule end time is %s', week_end_string)
        return week_end_string

    def get_title_info(self, uid):
        uid_list = self.uid_position_cache.keys()
        if uid in uid_list:
            return self.uid_position_cache[uid]
        else:
            title = self.mysql.get_uid_title_mapping(uid)
            self.uid_position_cache[uid] = title
            return title

    def dataframe_convert_datetime(self):
        scheduler_dataframe = schedule_df
        scheduler_dataframe['slot.from'] = pd.to_datetime(scheduler_dataframe['slot.from'])
        scheduler_dataframe['slot.to'] = pd.to_datetime(scheduler_dataframe['slot.to'])
        scheduler_dataframe['slot.date'] = pd.to_datetime(scheduler_dataframe['slot.date'])
        logging.debug('Convert slot.from, slot.to, slot.date to datetime type .')
        scheduler_dataframe['slot.date'] = scheduler_dataframe['slot.date'].apply(lambda x: datetime.datetime.date(x))
        scheduler_dataframe['slot.from'] = scheduler_dataframe['slot.from'].apply(lambda x: datetime.datetime.time(x))
        scheduler_dataframe['slot.to'] = scheduler_dataframe['slot.to'].apply(lambda x: datetime.datetime.time(x))
        return scheduler_dataframe

    def filter_storeid(self):
        dataframe = self.dataframe_convert_datetime()
        dataframe = dataframe[dataframe['storeId'].isin(self.storeid_list)]
        return dataframe

    def add_title_state_weekday_column(self, dataframe):
        dataframe['position_title'] = dataframe['slot.owner.uid'].apply(lambda uid: self.get_title_info(uid))
        dataframe['state'] = dataframe['storeId'].apply(lambda storeid: self.mysql.get_storeid_state_mapping(storeid))
        dataframe['weekday'] = dataframe['slot.date'].apply(lambda date: date.strftime("%a"))
        return dataframe


def main():
    begin_time = time.time()
    mongotopandas = MongoToPandas()

    start_time = '2018-07-10'
    end_time = '2018-07-15'
    dataframe = mongotopandas.generate_dataframe(start_time, end_time)
    print(dataframe.head)
    dataframe = mongotopandas.filter_storeid()
    dataframe2 = mongotopandas.add_title_state_weekday_column(dataframe)
    print(dataframe2.head())
    end_time = time.time()
    time_span = end_time - begin_time
    logging.debug('Convert date time type taken %s', time_span)


if __name__ == '__main__':
    main()





