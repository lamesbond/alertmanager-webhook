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