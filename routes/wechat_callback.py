#-*- coding:utf-8 -*-
from flask import Blueprint
import global_vars
from flask import request

from utils.wechat.WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
app_wechat_callback = Blueprint("app_wechat_callback",__name__)

@app_wechat_callback.route('/wechat_callback',methods=['GET','POST'])
def index():
    wxcpt=WXBizMsgCrypt(global_vars.WECHAT_APP_TOKEN,global_vars.WECHAT_ENCODINGAESKEY,global_vars.WECHAT_ENCODINGAESKEY)
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
            event_key = EventKey.text

        if event_key == 'acquire_alerts':
            global_vars.wechat_alertlist.send_msg(global_vars.wechat_access_token,global_vars.alert_dict)
        else:
            alertfingerprint = event_key
            response_code = global_vars.alert_dict[alertfingerprint]['status']
            global_vars.wechat_claim.send_msg(global_vars.wechat_access_token,response_code,claimant)
            global_vars.alert_dict[alertfingerprint]['status']=str(claimant)
            print("告警ID：",alertfingerprint,"已被",claimant,"认领")

    if( ret!=0 ):
        print("ERR: EncryptMsg ret: " + ret)
        sys.exit(1)
    return '认领成功'
