import json
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


    def send_msg(self,task_id,alertname,alertinstance,alertdesc):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",
            "toparty": " PartyID1 | PartyID2 ",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "template_card",
            "agentid": 1000002,
            "template_card" : {
                "card_type" : "text_notice",
                "main_title": {
                    "title": "告警"
                },
                "horizontal_content_list": [
                    {
                        "type": 0,
                        "keyname": "告警名称：",
                        "value": alertname
                    },
                    {
                        "type": 0,
                        "keyname": "告警主机：",
                        "value": alertinstance
                    },
                    {
                        "type": 0,
                        "keyname": "告警详情：",
                        "value": alertdesc
                    }
                ],
                "task_id": task_id,
            },
            "safe":0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        print(rep.text)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)

if __name__ == '__main__':
    wechat = WeChatPub()
    wechat.send_msg()
