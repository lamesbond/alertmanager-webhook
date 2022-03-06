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
            "msgtype": "template_card",
            "agentid": 1000002,
            "template_card" : {
                "card_type" : "text_notice",
                "source" : {
                    "icon_url": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png",
                    "desc": "企业微信",
                    "desc_color": 1
                },
                "action_menu": {
                    "desc": "卡片副交互辅助文本说明",
                    "action_list": [
                        {"text": "接受推送", "key": "A"},
                        {"text": "不再推送", "key": "B"}
                    ]
                },
                "task_id": "a001",
                "main_title" : {
                    "title" : "欢迎使用企业微信",
                    "desc" : "您的好友正在邀请您加入企业微信"
                },
                "quote_area": {
                    "type": 1,
                    "url": "https://work.weixin.qq.com",
                    "title": "企业微信的引用样式",
                    "quote_text": "企业微信真好用呀真好用"
                },
                "emphasis_content": {
                    "title": "100",
                    "desc": "核心数据"
                },
                "sub_title_text" : "下载企业微信还能抢红包！",
                "horizontal_content_list" : [
                    {
                        "keyname": "邀请人",
                        "value": "张三"
                    },
                    {
                        "type": 1,
                        "keyname": "企业微信官网",
                        "value": "点击访问",
                        "url": "https://work.weixin.qq.com"
                    }
                ],
                "jump_list" : [
                    {
                        "type": 1,
                        "title": "企业微信官网",
                        "url": "https://work.weixin.qq.com"
                    }
                ],
                "card_action": {
                    "type": 1,
                    "url": "https://work.weixin.qq.com",
                }
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