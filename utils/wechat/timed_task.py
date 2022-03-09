import datetime
import json
import requests
import global_vars


def update_wechat_access_token(WECHAT_CORP_ID,WECHAT_SECRET):

    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={WECHAT_CORP_ID}&corpsecret={WECHAT_SECRET}"
    s = requests.session()
    rep = s.get(url)
    if rep.status_code != 200:
        print("request failed.")
        return
    global_vars.wechat_access_token = json.loads(rep.content)['access_token']
    print("wechat_access_token已更新：", global_vars.wechat_access_token)

def check_alert_claims():
    for key in global_vars.alert_dict:
        if len(global_vars.alert_dict[key]['status']) >= 40:
            alertstartsat = global_vars.alert_dict[key]['alertstartsat'].replace(" CST","")
            interval_seconds = (datetime.datetime.now() - datetime.datetime.strptime(alertstartsat,"%Y-%m-%d %H:%M:%S")).seconds
            if interval_seconds >= 120:
                print("告警ID：",key,"已超过",interval_seconds,"秒都没人认领！！！")