# -*- coding:utf-8 -*-
from flask import Flask, request
import requests
import json
app = Flask(__name__)
'''
脚本功能：从192.168.111.1获取到json文件，然原样输出。

'''
@app.route('/send', methods=['POST'])
def send():
    try:
        data = json.loads(request.data)   #转换从alertmanager获得的json数据为dict类型
        print(data)
    except Exception as e:
        print(e)
    return 'ok'

if __name__ == '__main__':
 app.run(debug=False,host='0.0.0.0',port=5001)