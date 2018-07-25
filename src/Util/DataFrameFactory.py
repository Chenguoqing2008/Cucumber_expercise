#! /usr/bin/python3
# _*_ coding:utf-8 _*_

import pandas as pd
import numpy
import logging
import datetime
from db.MySql import MySql


class DataFrameFactory:
    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    dataframe = pd.DataFrame(columns=['dummy'])
    uid_position_cache = {}
    pd.set_option('mode.chained_assignment', None)
    mysql = MySql()

    def __init__(self, dataframe):
        DataFrameFactory.dataframe = dataframe

    @classmethod
    def dataframe_convert_datetime(cls):
        scheduler_dataframe = cls.dataframe
        scheduler_dataframe['slot.from'] = pd.to_datetime(scheduler_dataframe['slot.from'])
        scheduler_dataframe['slot.to'] = pd.to_datetime(scheduler_dataframe['slot.to'])
        scheduler_dataframe['slot.date'] = pd.to_datetime(scheduler_dataframe['slot.date'])
        logging.debug('Convert slot.from, slot.to, slot.date to datetime type .')
        scheduler_dataframe.loc[:, 'slot.date'] = scheduler_dataframe.loc[:, 'slot.date']\
            .apply(lambda x: datetime.datetime.date(x))
        scheduler_dataframe['slot.from'] = scheduler_dataframe['slot.from']\
            .apply(lambda x: datetime.datetime.time(x))
        scheduler_dataframe.loc[:, 'slot.to'] = scheduler_dataframe.loc[:, 'slot.to']\
            .apply(lambda x: datetime.datetime.time(x))
        return cls(scheduler_dataframe)

    @classmethod
    def filter_storeid(cls):
        storeid_list = cls.mysql.get_storeid()
        logging.debug("Storeid list is %s", storeid_list)
        dataframe_filter_storeid = cls.dataframe[cls.dataframe['storeId'].isin(storeid_list)]
        filter_storeid_series = dataframe_filter_storeid[['storeId']]
        unique_storeid_list = numpy.unique(numpy.array(filter_storeid_series)[:, 0])
        logging.debug('Filter storeId is done, valid storeId is %s', unique_storeid_list)
        return cls(dataframe_filter_storeid)

    @classmethod
    def add_state_column(cls):
        dataframe_state = cls.dataframe
        storeid_state_map = cls.mysql.generate_storeid_state_map()
        dataframe_state['state'] = dataframe_state['storeId'] \
            .apply(lambda storeId: storeid_state_map.get(storeId))
        return cls(dataframe_state)

    @classmethod
    def add_title_column(cls):
        dataframe_title = cls.dataframe
        uid_list = dataframe_title['slot.owner.uid'].unique()
        unique_uid = [str(_) for _ in uid_list]
        uid_title_map = cls.mysql.generate_uid_title_map(unique_uid)
        dataframe_title['position_title'] = dataframe_title['slot.owner.uid'] \
            .apply(lambda uid: uid_title_map.get(uid))
        return cls(dataframe_title)

    @classmethod
    def add_weekday_column(cls):
        dataframe_weekday = cls.dataframe
        dataframe_weekday['weekday'] = dataframe_weekday['slot.date'] \
            .apply(lambda date: date.strftime("%a"))
        return cls(dataframe_weekday)

