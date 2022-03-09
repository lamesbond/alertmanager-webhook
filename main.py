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
    requests.post()
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.run()  # 启动flask