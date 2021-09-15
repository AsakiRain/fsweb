import datetime
strTime = '2021-09-15 20:56:39'
startTime = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
print(startTime)
now_time = datetime.datetime.now().replace(microsecond=0)
print(now_time)
if now_time > startTime:
    print('过期')