#-*- coding:utf-8 -*-
from flask import Flask,request
from WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
import json
import uuid

from wechatsend_claim import WeChatPub as WeChatPub_claim
from wechatsend_firing import WeChatPub as WeChatPub_firing
from wechatsend_firing import WeChatPub as WeChatPub_resolved

app = Flask(__name__)
alert_dict={}
wechat_firing = WeChatPub_firing()
wechat_resolved = WeChatPub_resolved()
wechat_claim = WeChatPub_claim()

@app.route('/wechat_callback',methods=['GET','POST'])
def index():
    s_token = "zI49d9BrPYP6nPH6GfkbHuHiTunQLonF"
    s_encoding_asekey = "cMklFT1ZeRUf8r2Dh4ofh7vqseX9ZPTbusJMZG1mDvX"
    s_corp_id = "wwd4c0cabaa5479e2b"
    wxcpt=WXBizMsgCrypt(s_token,s_encoding_asekey,s_corp_id)
    #获取url验证时微信发送的相关参数
    sVerifyMsgSig=request.args.get('msg_signature')
    sVerifyTimeStamp=request.args.get('timestamp')
    sVerifyNonce=request.args.get('nonce')
    sVerifyEchoStr=request.args.get('echostr')

    if request.method == 'GET':
        ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
        print(type(ret))
        print(type(sEchoStr))
        if (ret != 0 ):
            print("ERR: VerifyURL ret:" + ret)
            sys.exit(1)
        return sEchoStr
    #接收客户端消息
    if request.method == 'POST':
        sReqMsgSig = sVerifyMsgSig
        sReqTimeStamp = sVerifyTimeStamp
        sReqNonce = sVerifyNonce
        sReqData = request.data

        ret,sMsg=wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)

        if (ret != 0):
            print("ERR: VerifyURL ret:")
            sys.exit(1)

        xml_tree = ET.fromstring(sMsg)
        for FromUserName in xml_tree.findall('FromUserName'):
            claimant = FromUserName.text
#        for response_code in xml_tree.findall('ResponseCode'):
#            response_code = response_code.text
        for EventKey in xml_tree.findall('EventKey'):
            alertfingerprint = EventKey.text

        response_code = alert_dict[alertfingerprint]
        wechat_claim.send_msg(response_code,claimant)
        alert_dict[alertfingerprint]='claimed'
        print("告警ID：",alertfingerprint,"已被",claimant,"认领")

    if( ret!=0 ):
        print("ERR: EncryptMsg ret: " + ret)
        sys.exit(1)
    return '认领成功'

@app.route('/wechat_send', methods=['POST'])
def send():
    try:
        data = json.loads(request.data)
        alerts = data['alerts']

        for i in alerts:
            labels = i.get('labels')
            task_id = str(uuid.uuid1())
            alertstatus = i.get('status')
            alertfingerprint = i.get('fingerprint')
            alertname = labels['alertname']
            alertinstance = labels['instance']
            alertdesc = i.get('annotations').get('description')

            if alertstatus == 'firing':
                if alertfingerprint in alert_dict.keys() and alert_dict[alertfingerprint] == 'claimed':
                    print("告警", alertfingerprint, "已被认领，将不会发送")
                    continue
                else:
                    response_code = wechat_firing.send_msg(task_id, alertfingerprint, alertname, alertinstance, alertdesc)['response_code']
                    alert_dict[alertfingerprint] = response_code
            if alertstatus == 'resolved':
                wechat_resolved.send_msg()
                alert_dict[alertfingerprint] = 'resolved'

        print("fingerprint与response code对应表：",alert_dict)
    except Exception as e:
        print(e)
    return '发送成功'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9096,debug=True)
