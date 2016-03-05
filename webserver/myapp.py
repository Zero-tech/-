# -*- coding:utf8 -*-
from flask import Flask, g, request, make_response
import hashlib
from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#加载app入口模块
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "Hello, world! by Zero-tech"

#与微信对应的 token数组
access_token = 'hellozerotech'
# 实例化 wechat，这是个全局变量
wechat = WechatBasic(token=access_token)
#全局的消息响应
responeCase = {}
#动态生成的装饰器，即使用函数封装的装饰器
#用于传入与type相同类型的 参数， 并调用
def responeMessage(type):
    #装饰器
    def decorator(func):
        #利用装饰器，把类型和函数，通过字典联系起来，便于编程
        responeCase[type] = func
        def warapper(instance):
            if(type is instance.__class__):
                return func(instance)
            else:
                return "Error"
        return warapper
    return decorator

#处理文本消息
@responeMessage(TextMessage)
def handleText(message):
    return wechat.response_text(u'文字')


@app.route('/weibo/', methods=['POST', 'GET'])
def wechatHandler():
    #get 方式用于服务器 token认证
    if request.method == 'GET':
        #获取GET传参
        query = request.args
        sign = query.get('signature', '')
        stamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [stamp, nonce, access_token]
        s.sort()
        s = ''.join(s)
        if(hashlib.sha1(s).hexdigest() == sign):
            return make_response(echostr)
        else:
            return "weibo auth failed!!"
    #POST 为消息接收
    elif request.method == 'POST':
        #URL 传参
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        #POST 传输的数据体
        body_text = request.data
        # 对签名进行校验
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
            wechat.parse_data(body_text)
            # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
            message = wechat.get_message()

            '''
            responseData = None
            if message.type == 'text':
                if message.content == 'wechat':
                    responseData = wechat.response_text(u'^_^')
                else:
                    responseData = wechat.response_text(u'文字')
            elif message.type == 'image':
                responseData = wechat.response_text(u'图片')
            else:
                responseData = wechat.response_text(u'未知')
            '''
            if message.__class__ not in responeCase.keys():
                responseData = wechat.response_text(u'未知')
            else:
                responseData = responeCase[message.__class__](message)
            # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可
            response = make_response(responseData)
            response.content_type = 'application/xml'
            return response


#应用程序启动
if __name__ == '__main__':
    #这会让操作系统监听所有公网 IP。
    app.run(host='0.0.0.0', port=5000)