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


    def send_msg(self,response_code,claimant):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/update_template_card?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "atall" : 1,
            "agentid" : 1000002,
            "response_code": response_code,
            "button":{
                "replace_name": "认领人："+str(claimant)
            }
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
