import json
import requests
class WeChatPub:
    s = requests.session()

    def send_msg(self,wechat_access_token,alertlist="none"):
        if not alertlist:
            context = "暂无告警"
        else:
            context = "#  <font color=\"warning\">告警列表：</font>\n"
            for key in alertlist:
                if alertlist[key]['status'] == 'resolved':
                    continue
                else:
                    context=context+"\n告警ID："+key+"\n告警状态："+alertlist[key]['status']+"\n<font color=\"warning\">告警名称：</font>"+alertlist[key]['alertname']+"\n告警主机："+alertlist[key]['alertinstance']+"\n告警详情："+alertlist[key]['alertdesc']+"<br/>"
            if not context:
                context = "告警已解决"

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
                "content": context
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
