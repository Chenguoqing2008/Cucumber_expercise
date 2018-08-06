#! /usr/bin/python3
# _*_ coding:utf-8 _*_

import datetime
import logging


class DateInfo:
    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    
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
