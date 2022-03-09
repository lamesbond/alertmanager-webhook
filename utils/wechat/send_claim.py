import json
import requests

class WeChatPub:
    s = requests.session()

    def send_msg(self,wechat_access_token,response_code,claimant):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/update_template_card?access_token=" + wechat_access_token
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
