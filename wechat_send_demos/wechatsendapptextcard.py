import json
import datetime
import requests

CORP_ID = "wwd4c0cabaa5479e2b"
SECRET = "fgAXG0M1E-VOYJH-oA2_aCCdV1YKL28njGHKb_XtLLo"

class WeChatPub:
    s = requests.session()

    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
        rep = self.s.get(url)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)['access_token']


    def send_msg(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",
            "toparty": " PartyID1 | PartyID2 ",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "textcard",
            "agentid": 1000002,
            "textcard" : {
            "title" : "领奖通知",
            "description" : "<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">恭喜你抽中iPhone 7一台，领奖码：xxxx</div><div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>",
            "url" : "URL",
                        "btntxt":"更多"
            },
            "safe":0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)

if __name__ == '__main__':
    wechat = WeChatPub()
    wechat.send_msg()