#! /usr/bin/python
# _*_ coding:utf-8 _*_

from util.MongoToPandas import MongoToPandas
from util.DataFrameFactory import DataFrameFactory
from util.MongoToPandas import run_mongo_converter


class ScheduleObject:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.mongotopandas = MongoToPandas()
        date_str_list = self.mongotopandas.generate_date_list(self.start_date, self.end_date)
        output_queue = run_mongo_converter(date_str_list)
        self.dataframe_base = self.mongotopandas.get_base_dataframe(output_queue)
        self.shedule_dataframe = DataFrameFactory(self.dataframe_base) \
            .filter_storeid() \
            .dataframe_convert_datetime() \
            .add_title_column() \
            .add_state_column() \
            .add_weekday_column().dataframe

