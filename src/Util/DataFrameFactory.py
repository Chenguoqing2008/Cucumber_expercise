#! /usr/bin/python3
# _*_ coding:utf-8 _*_

import pandas as pd
import datetime
import logging
from db.MySql import MySql


class DataFrameFactory(MySql):
    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    dataframe = pd.DataFrame(columns=['dummy'])
    uid_position_cache = {}

    def __init__(self, dataframe):
        DataFrameFactory.dataframe = dataframe

    @classmethod
    def dataframe_convert_datetime(cls):
        scheduler_dataframe = cls.dataframe
        scheduler_dataframe.loc[:, 'slot.from'] = scheduler_dataframe.astype(datetime)
        # scheduler_dataframe.loc[:, 'slot.from'] = pd.to_datetime(scheduler_dataframe.loc[:, 'slot.from'])
        # scheduler_dataframe.loc[:, 'slot.to'] = pd.to_datetime(scheduler_dataframe.loc[:, 'slot.to'])
        # scheduler_dataframe.loc[:, 'slot.date'] = pd.to_datetime(scheduler_dataframe.loc[:, 'slot.date'])
        # logging.debug('Convert slot.from, slot.to, slot.date to datetime type .')
        # scheduler_dataframe.loc[:, 'slot.date'] = scheduler_dataframe.loc[:, 'slot.date']\
        #     .apply(lambda x: datetime.datetime.date(x))
        scheduler_dataframe.loc[:, 'slot.from'] = scheduler_dataframe.loc[:, 'slot.from']\
            .apply(lambda x: datetime.datetime.time(x))
        #  scheduler_dataframe.loc[:, 'slot.from'] = scheduler_dataframe.loc[:, 'slot.from']\
        #     .apply(lambda x: datetime.datetime.time(x))
        # scheduler_dataframe.loc[:, 'slot.to'] = scheduler_dataframe.loc[:, 'slot.to']\
        #     .apply(lambda x: datetime.datetime.time(x))
        return cls(scheduler_dataframe)

    # @classmethod
    # def filter_storeid(cls, storeid_list):
    #     dataframe_filter_storeid = cls.dataframe[cls.dataframe['storeId'].isin(storeid_list)]
    #     # logging.debug('Filter storeId is done, valid storeId is', cls.dataframe['storeId'])
    #     return cls(dataframe_filter_storeid)

    @classmethod
    def filter_storeid(cls, storeid_list):
        dataframe_filter_storeid = cls.dataframe[cls.dataframe['storeId'].isin(storeid_list)]
        # logging.debug('Filter storeId is done, valid storeId is', cls.dataframe['storeId'])
        return cls(dataframe_filter_storeid)

    @classmethod
    def add_title_state_weekday_column(cls):
        dataframe_columns = cls.dataframe
        dataframe_columns['position_title'] = dataframe_columns['slot.owner.uid']\
            .apply(lambda uid: cls.get_title_info(uid))
        dataframe_columns['state'] = dataframe_columns['storeId']\
            .apply(lambda storeid: super().get_storeid_state_mapping(storeid))
        dataframe_columns['weekday'] = dataframe_columns['slot.date']\
            .apply(lambda date: date.strftime("%a"))
        return cls(dataframe_columns)

    @classmethod
    def get_title_info(cls, uid):
        uid_list = cls.uid_position_cache.keys()
        if uid in uid_list:
            return cls.uid_position_cache[uid]
        else:
            title = super().get_uid_title_mapping(uid)
            cls.uid_position_cache[uid] = title
            return title
