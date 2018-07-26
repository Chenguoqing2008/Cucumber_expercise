#! /usr/bin/python

import datetime
from db.MongoDb import MongoDb
import locale
import time
import pandas as pd

# time1 = locale.getlocale()
#
# print(time1)

date_str = '2018-07-16'
date1 = datetime.datetime.strptime(date_str, '%Y-%m-%d')
print(date1.strftime("%a,%d %B, %y"))
print(date1.strftime("%a"))
# calendar = date1.isocalendar()
# year_test = calendar[0]
# week_test = calendar[1]
# day_test = calendar[2]

# date_string = str(year_test) + '-' + str(week_test) + '-' + str(day_test)
# time_test = datetime.datetime.strptime(date_string, '%Y-%W-%w').date()
# time_test = datetime.datetime.strptime(day_test, '%A')
# print(time_test)
# print(date_str)
# print(year_test)
# print(week_test)
# print(day_test)

# now = datetime.datetime.now()
# print(now.strftime("%a,%d %B, %y"))

start_date = '2018-07-10'
end_date = '2018-07-15'
start_time = time.time()
mongodb = MongoDb()
result = mongodb.get_time_span_data(start_date, end_date, 5)
for i in range(len(result)):
    print(result[0])
    print('\n')
print(result)
# print(type(result))
# print(result.__len__())
end_time = time.time()
time_span = end_time - start_time
print(time_span)
# print(result)

# rng = pd.date_range('3/6/2012', periods=5, freq='D')
# print(rng.__len__())
# print(rng[4])
# t1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
# t2 = datetime.datetime.strptime(end_date, '%Y-%m-%d')
# print(type((t2-t1).days))
# for index in range((t2-t1).days+1):
#     time_index = t1 + datetime.timedelta(days=index)
#     print(datetime.datetime.strftime(time_index, '%Y-%m-%d'))

# print(t2 - t1).

