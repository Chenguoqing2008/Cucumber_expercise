#! /usr/bin/python

import datetime

date1 = datetime.datetime.strptime()
calendar = date1.isocalendar()
year_test = calendar[0]
week_test = int(calendar[1])-1
day_test = 0

date_string = str(year_test) + '-' + str(week_test) + '-' + str(day_test)
time_test = datetime.datetime.strptime(date_string, '%Y-%W-%w').date()

print(time_test)

print(year_test)
print(week_test)
print(day_test)

