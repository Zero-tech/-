# -*- coding:utf8 -*-
from flask import Flask, g, request, make_response
import  hashlib

#加载app入口模块
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "Hello, world! - Flask"

@app.route('/weibo/', methods=['POST', 'GET'])
def wechat_auth():
    if request.method == 'GET':
        #与微信对应的 token数组
        token = 'hellozerotech'
        #获取GET传参
        query = request.args
        print query
        sign = query.get('signature', '')
        stamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [stamp, nonce, token]
        s.sort()
        s = ''.join(s)
        print s
        if(hashlib.sha1(s).hexdigest() == sign):
            return make_response(echostr)
        else:
            return "weibo auth failed!!"

#应用程序启动
if __name__ == '__main__':
    #这会让操作系统监听所有公网 IP。
    app.run(host='0.0.0.0', port=5000)