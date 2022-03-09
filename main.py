import time
import datetime
import pytz

import requests
from flask_apscheduler import APScheduler
from flask import Flask


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:job_1',
            'args': (1, 2),
            'trigger': 'cron',
            'hour': 17,
            'minute': 8
        },
        {
            'id': 'job2',
            'func': '__main__:job_1',
            'args': (3, 4),
            'trigger': 'interval',
            'seconds': 5
        }
    ]


def job_1(a, b):  # 一个函数，用来做定时任务的任务。
    print(str(a) + ' ' + str(b))


app = Flask(__name__)  # 实例化flask

app.config.from_object(Config())  # 为实例化的flask引入配置


@app.route('/')  # 首页路由
def hello_world():
    return 'hello'


if __name__ == '__main__':
    startsat = "2022-03-09T13:55:54.343Z"
    # startsattimestamp=time.mktime(time.strptime(startsat, "%Y-%m-%dT%H:%M:%S.%fZ"))
    # startsat_normal=datetime.utcfromtimestamp(startsattimestamp).strftime("%Y-%m-%d %H:%M:%S")
    # print(startsat_normal)

    d1 = datetime.datetime.strptime(startsat,"%Y-%m-%dT%H:%M:%S.%fZ")
    d8 = (datetime.datetime.strptime(startsat,"%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8))
    # d9 = datetime.datetime.strptime(d8,"%Y-%m-%d %H:%M:%S")
    print(d8)
    d2 = datetime.datetime.now()
    if isinstance(d8,str):
        print("是世家格式")
    interval = d2-d8
    print(interval)
    interval_min = interval.seconds
    print(interval_min)
    if isinstance(interval_min,int):
        print("intercalmin是证书")

    zfc='2022-03-09 23:10:54 CST'
    print(zfc.replace(" CST",""))
    print(len(zfc))
    print(len(zfc.replace(" CST","")))

        # .astimezone(timezone(timedelta(hours=16)))
    # print(str(start))
    # # current_time = (datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    # # print(str(current_time))
    # if isinstance(start, datetime):
    #     print("是时间格式")
    # elif isinstance(start, str):
    #     print("是字符串")