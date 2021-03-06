import json
import requests

class WeChatPub:
    s = requests.session()

    def send_msg(self,wechat_access_token,task_id,alertfingerprint,alertname,alertinstance,alertdesc,alertstartsat):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + wechat_access_token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser" : "@all",
            "toparty" : "PartyID1 | PartyID2",
            "totag" : "TagID1 | TagID2",
            "msgtype" : "template_card",
            "agentid" : 1000002,
            "template_card" : {
                "card_type" : "button_interaction",
                "main_title" : {
                    "title" : "告警"
                },
                "horizontal_content_list" : [
                    {
                        "type" : 0,
                        "keyname" : "告警名称：",
                        "value" : alertname
                    },
                    {
                        "type": 0,
                        "keyname": "告警主机：",
                        "value": alertinstance
                    },
                    {
                        "type": 0,
                        "keyname": "告警详情：",
                        "value" : alertdesc
                    },
                    {
                        "type": 0,
                        "keyname": "开始时间：",
                        "value" : alertstartsat
                    }
                ],
                "task_id": task_id,
                "button_list": [
                    {
                        "text": "认领",
                        "style": 2,
                        "key": alertfingerprint
                    }
                ]
            },
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
