#! /usr/bin/python
# _*_ coding:utf-8 _*_

from util.ScheduleObject import ScheduleObject

start_date = '2018-07-10'
end_date = '2018-07-15'
scheduleobject = ScheduleObject(start_date, end_date)
print(scheduleobject.schedule_dataframe.shape)
print(scheduleobject.schedule_dataframe.head(0))
print(scheduleobject.schedule_dataframe.head(5))









