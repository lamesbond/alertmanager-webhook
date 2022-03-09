#-*- coding:utf-8 -*-
import datetime
import json
import time
import uuid

from flask import request, Blueprint

import global_vars

app_wechat_send = Blueprint("wechat_send",__name__)
@app_wechat_send.route('/wechat_send', methods=['POST'])
def send():
    try:
        data = json.loads(request.data)
        alerts = data['alerts']

        for i in alerts:
            task_id = str(uuid.uuid1())
            alertstatus = i['status']
            alertfingerprint = i['fingerprint']
            alertname = i['labels']['alertname']
            alertinstance = i['labels']['instance']
            alertdesc = i['annotations']['description']
            alertstartsat = (datetime.datetime.strptime(i['startsAt'],"%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")+" CST"

            global_vars.alert_dict[alertfingerprint] = {}
            global_vars.alert_dict[alertfingerprint]['alertname'] = alertname
            global_vars.alert_dict[alertfingerprint]['alertinstance'] = alertinstance
            global_vars.alert_dict[alertfingerprint]['alertdesc'] = alertdesc
            global_vars.alert_dict[alertfingerprint]['alertstartsat'] = alertstartsat

            if alertstatus == 'firing':
                if alertfingerprint in global_vars.alert_dict.keys() and global_vars.alert_dict[alertfingerprint] == 'claimed':
                    print("告警", alertfingerprint, "已被认领，将不会发送")
                    continue
                else:
                    response_code = global_vars.wechat_firing.send_msg(global_vars.wechat_access_token,task_id, alertfingerprint, alertname, alertinstance, alertdesc,alertstartsat)['response_code']
                    global_vars.alert_dict[alertfingerprint]['status'] = response_code
            if alertstatus == 'resolved':
                global_vars.wechat_resolved.send_msg(global_vars.wechat_access_token,alertname, alertinstance, alertdesc,alertstartsat)
                global_vars.alert_dict[alertfingerprint]['status'] = 'resolved'

    except Exception as e:
        print(e)
    return '发送成功'