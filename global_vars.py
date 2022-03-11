#-*- coding:utf-8 -*-
from flask import Flask

from utils.wechat.send_claim import WeChatPub as WeChatPub_claim
from utils.wechat.send_firing import WeChatPub as WeChatPub_firing
from utils.wechat.send_resolved import WeChatPub as WeChatPub_resolved
from utils.wechat.send_alertlist import WeChatPub as WeChatPub_alertlist

WECHAT_CORP_ID = "wwd4c0cabaa5479e2b"
WECHAT_SECRET = "fgAXG0M1E-VOYJH-oA2_aCCdV1YKL28njGHKb_XtLLo"
WECHAT_APP_TOKEN = "zI49d9BrPYP6nPH6GfkbHuHiTunQLonF"
WECHAT_ENCODINGAESKEY = "cMklFT1ZeRUf8r2Dh4ofh7vqseX9ZPTbusJMZG1mDvX"
wechat_access_token=""

app = Flask(__name__)

alert_dict={}
wechat_firing = WeChatPub_firing()
wechat_resolved = WeChatPub_resolved()
wechat_claim = WeChatPub_claim()
wechat_alertlist = WeChatPub_alertlist()