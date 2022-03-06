
from flask import app, jsonify, Flask, request
import sys
from WXBizMsgCrypt3 import WXBizMsgCrypt
app = Flask(__name__)

class AuthVerify(object):

    def verify(self, msg_signature, timestamp, nonce, echostr):
        s_token = "zI49d9BrPYP6nPH6GfkbHuHiTunQLonF"
        s_encoding_asekey = "cMklFT1ZeRUf8r2Dh4ofh7vqseX9ZPTbusJMZG1mDvX"
        s_corp_id = "wwd4c0cabaa5479e2b"
        wxcpt = WXBizMsgCrypt(s_token, s_encoding_asekey, s_corp_id)
        ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        print("ret:",ret)
        print(sEchoStr)
        if ret != 0:
            print("ERR: VerifyURL ret: " + str(ret))
            sys.exit(1)
        else:
            return sEchoStr

@app.route('/', methods=['POST','GET'])
def receive():
    try:

        msg_signature = request.args.get('msg_signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        auth_verify = AuthVerify()

        s_echo_str = auth_verify.verify(msg_signature, timestamp, nonce, echostr)
        return s_echo_str
    except Exception as e:
        print(e)
        return jsonify({'code': -1, 'error_message': e})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)