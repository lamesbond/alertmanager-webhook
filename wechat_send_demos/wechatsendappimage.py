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
            "msgtype": "image",
            "agentid": 1000002,
            "image" : {
                "media_id": "3rPvOBFNgAw7UAaEcIzk4O87PB7lTAp7S7TdtuG65KzheLjOOQKit4j31PsfbhRo5"
            },
            "safe":0,
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