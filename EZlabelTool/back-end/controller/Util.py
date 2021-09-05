# -*- coding:utf-8 -*-
# Date: 07 April 2021
# Author：Pingyi Hu a1805597
# Description：Implement some useful tools

import datetime
import time

# '2015-08-28 16:43:37.283' --> 1440751417.283 or '2015-08-28 16:43:37' --> 1440751417.0
# turn a time string into timestamp
def string2timestamp(strValue):
 
    try:        
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000
        # print (timeStamp)
        return timeStamp
    except ValueError as e:
        print (e)
        d = datetime.datetime.strptime(str2, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000
        # print (timeStamp)
        return timeStamp


# to show the time since your last modified
# Input: time string: '2015-08-28 16:43:37.283' ---- last modified time
# if dif < 10days, show dif info
# dif < 1 min, show seconds ---- '30s ago'
# dif < 1 hour, show mins + seconds ---- '5mins 30s ago'
# dif < 24 hours, show hours + mins ---- '12hours 34mins ago'
# dif < 7 days, show days + hours ---- '5days 10hours ago'
# else show last modified time  ---- '09 Jan 2021'
def last_modify(modify_time):
	now = datetime.datetime.now()
	nowstamp = now.timestamp()
	laststamp = string2timestamp(modify_time)
	dif = int(nowstamp - laststamp)

	if dif < 60:
		res = str(dif) + 's ago'

	elif dif < 3600:
		seconds = int(dif%60)
		mins = int(dif/60)
		res = str(mins) + 'mins ' + str(seconds) + 's ago'

	elif dif < 86400:
		mins = int((dif%3600)/60)
		hours = int(dif/3600)
		res = str(hours) + 'hours ' + str(mins) + 'mins ago'

	elif dif < 604800:
		hours = int((dif%86400)/3600)
		days = int(dif/86400)
		res = str(days) + 'days ' + str(hours) + 'hours ago'

	else:
		last_modifed_time = time.strftime("%d %b %Y", time.localtime(laststamp))
		res = str(last_modifed_time)
	return res


def calcu_label_time(start_time, end_time):
	StartStamp = string2timestamp(start_time)
	EndStamp = string2timestamp(end_time)
	dif = int(EndStamp - StartStamp)
	return(dif)

def difToTime(dif):
	if dif < 60:
		res = str(dif) + 's'
	elif dif < 3600:
		seconds = int(dif%60)
		mins = int(dif/60)
		res = str(mins) + 'mins ' + str(seconds) + 's'
	elif dif < 86400:
		mins = int((dif%3600)/60)
		hours = int(dif/3600)
		res = str(hours) + 'hours ' + str(mins) + 'mins'
	elif dif < 604800:
		hours = int((dif%86400)/3600)
		days = int(dif/86400)
		res = str(days) + 'days ' + str(hours) + 'hours'
	return res


################ test #################
# t = last_modify('2021-04-02 17:21:01.898526')
# print(t)