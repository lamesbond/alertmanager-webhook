#-*- coding:utf-8 -*-
from flask_apscheduler import APScheduler
from global_vars import WECHAT_CORP_ID, WECHAT_SECRET, app
from routes.wechat_callback import app_wechat_callback
from routes.wechat_send import app_wechat_send
from routes.metrics import app_metrics
from utils.wechat.update_access_token import update_wechat_access_token

app.register_blueprint(app_wechat_callback)
app.register_blueprint(app_wechat_send)
app.register_blueprint(app_metrics)

class Config(object):
    JOBS = [
        {
            'id': 'update_wechat_access_token',
            'func': '__main__:update_wechat_access_token',
            'args': (WECHAT_CORP_ID, WECHAT_SECRET),
            'trigger': 'interval',
            'seconds': 7200
        }
    ]

app.config.from_object(Config())

if __name__ == '__main__':
    update_wechat_access_token(WECHAT_CORP_ID, WECHAT_SECRET)
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.run(host='0.0.0.0',port=9096,debug=True)
