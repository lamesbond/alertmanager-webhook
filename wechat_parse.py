#-*- coding:utf-8 -*-
from flask import Flask,request
from WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
import json
import uuid

from wechat_send_demos.wechatsendapptemplate_card_button_interaction_update import WeChatPub as WeChatPub_update
from wechat_send_demos.wechatsendapptemplate_card_button_interaction import WeChatPub as WeChatPub_send

app = Flask(__name__)
claim_list = []
response_code_list = []

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
        for claimant in xml_tree.findall('FromUserName'):
            print("认领人：",claimant.text)
        for response_code in xml_tree.findall('ResponseCode'):
            response_code = response_code.text
        for event_key in xml_tree.findall('EventKey'):
            event_key = event_key.text
        print("EventKey：",event_key,"已被认领")
        claim_list.append(event_key)

        wechat = WeChatPub_update()
        for response_code in response_code_list:
            wechat.send_msg(response_code,claimant.text)

    if( ret!=0 ):
        print("ERR: EncryptMsg ret: " + ret)
        sys.exit(1)
    return

@app.route('/wechat_send', methods=['POST'])
def send():
    try:
        data = json.loads(request.data)
        alerts = data['alerts']

        for i in alerts:
            info = i.get('labels')
            task_id = str(uuid.uuid1())
            alertfingerprint = i.get('fingerprint')
            alertname = info['alertname']
            alertinstance = info['instance']
            alertservice = info['service']
            alertdesc = i.get('annotations')['description']
            print(alertname)
            print(alertinstance)
            print(alertservice)
            print(alertdesc)
            if alertfingerprint in claim_list:
                print("告警",alertfingerprint,"已被认领，将不会发送")
                return 200
            wechat = WeChatPub_send()
            response_code = wechat.send_msg(task_id,alertfingerprint,alertname,alertinstance,alertservice,alertdesc)
            response_code_list.append(response_code.get('response_code'))
            print(response_code_list)
    except Exception as e:
        print(e)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)