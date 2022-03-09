import json
import requests

class WeChatPub:
    s = requests.session()

    def send_msg(self,wechat_access_token,alertname,alertinstance,alertdesc,alertstartsat):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + wechat_access_token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser" : "@all",
            "toparty" : "PartyID1|PartyID2",
            "totag" : "TagID1 | TagID2",
            "msgtype": "markdown",
            "agentid": 1000002,
            "markdown": {
                "content": "### <font color=\"info\">恢复</font>\n"
                    "告警名称：" + alertname + "\n"
                    "告警主机：" + alertinstance + "\n"
                    "告警详情：" + alertdesc + "\n"
                    "开始时间：" + alertstartsat + "\n"
            },
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        print(rep.text)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)
