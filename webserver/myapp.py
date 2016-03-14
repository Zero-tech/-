# -*- coding:utf8 -*-
from flask import Flask, g, request, make_response
import hashlib
from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)
from tulingTest import Tl123, MsgTl123, TextMsgtl123, Tl123Util
from DbHandler import DbHandler
from QrcodeHandler import QrcodeHandler
from EasySession import Session
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#加载app入口模块
app = Flask(__name__)
app.debug = True
handle = DbHandler()
#不能提前挂起，随后在数据的到来时，再操作SQL数据库，否则会发起超时关闭。
#handle.connect()
#handle.insert('12345', 123465, 'UNACTIVE', 'OFF', 'Temp=21&Humi=35&Light=OFF')

print 'Run the app, and init the flask,db moudle!!'

@app.route('/')
def hello():
    return "Hello, world! by Zero-tech"

#数据库操作
@app.route('/db')
def db_op():
    '''
    数据库请求操作，可以增改数据项，返回接送数据，格式如下：
        {
            code: x.
            info: ""
        }:
    code 表示类型码，0位正确，非0位错误。
        1，没有操作类型， Unknown operate types
        2，没有操作类型， Unsupport operate type
        3  数据库异常     Database exception
    '''
    rspJson = dict(info='None', code=0)
    if request.method == 'GET':
        args = request.args
        op = args.get('Op', '')
        if op == None:
            rspJson['code'] = 1
            rspJson['info'] = 'Unknown operate types'
            return make_response(json.dumps(rspJson))
        #连接数据库
        handle.connect()
        text = None
        try:
            if op == 'Insert':
                mac = args.get('MAC', '')
                text = handle.insert(mac)
            elif op == 'Bind':
                mac = args.get('MAC', '')
                userid = args.get('UserID', '')
                text = handle.deviceBind(mac, userid)
            elif op == 'Unbind':
                mac = args.get('MAC', '')
                userid = args.get('UserID', '')
                text = handle.deviceUnbind(mac, userid)
            elif op == 'UpdateInfo':
                mac = args.get('MAC', '')
                userid = args.get('UserID', '')
                info = args.get('Info', '')
                text = handle.deviceUpdateInfo(mac, userid, info)
            elif op == 'Off':
                mac = args.get('MAC', '')
                userid = args.get('UserID', '')
                text = handle.deviceOff(mac)
            elif op == 'Query':
                mac = args.get('MAC', '')
                text = handle.deviceQuery(mac)
            else:
                rspJson['code'] = 2
                rspJson['info'] = 'Unsupport operate type'
                #操作完成，关闭数据库
                handle.close()
                return make_response(json.dumps(rspJson))
            rspJson['code'] = 0
            rspJson['info'] = str(text)
            text = json.dumps(rspJson)
        except Exception, e:
            rspJson['code'] = 3
            rspJson['info'] = str(e)
            text = json.dumps(rspJson)
        #操作完成，关闭数据库
        handle.close()
        return make_response(text)

#设备api测试
@app.route('/DeviceServer', methods=['GET', 'POST'])
def DeviceServer():
    if request.method == 'GET':
        args = request.args
        mac = args.get('MAC', '')
        temp = args.get('temp', '')
        humi = args.get('humi', '')
        light = args.get('light', '')
        if mac == '' or temp == '' or humi == '' or light == '':
            return make_response('Wrong Param!')
        if light == 'on':
            light = 'off'
        else:
            light = 'on'
        print 'yes i got the Device info, that temp is %s, humi is %s, light is %s!'%(temp, humi, light)
        return make_response('light='+light)
    else:
        return make_response('Wrong Request Method!')

#实例化全局的图灵机器人
tl = Tl123()

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
    #return wechat.response_text(u'文字')
    handle.connect()
    rsp = handle.userQuery(message.source)
    if rsp != None:
        session = Session(message.source)
        session.state = rsp[0][1]
        handle.close()
        rspFromSession = handleSession(session, message.content)
        if rspFromSession != u'未知指令':
            return wechat.response_text(rspFromSession)

    if message.content == u'绑定设备':
        handle.userInsert(message.source, Session.session_states[0])
        handle.close()
        return wechat.response_text(u'请发送绑定设备的二维码')
    handle.close()
    return wechat.response_text(tl.requestMsg(message.content).text)

#处理图片消息
@responeMessage(ImageMessage)
def handleImage(message):
    print message.picurl
    pars = QrcodeHandler.parse(message.picurl)
    '''if  rsp== None:
        return wechat.response_text(u'不是qrcode哦')'''
    handle.connect()
    rsp = handle.userQuery(message.source)
    if rsp != None:
        session = Session(message.source)
        session.state = rsp[0][1]
        handle.close()
        return wechat.response_text(handleSession(session, pars))

    handle.close()
    return wechat.response_text(rsp)


#处理会话
def handleSession(session, text):
    #处理 unbind
    if session.state == Session.session_states[0]:
        try:
            tmp = json.loads(text)
        except Exception, e:
            return u'请发送正确的设备格式\n'+str(e)+str(text)
        mac = tmp['MAC']
        handle.connect()

        n = handle.deviceBind(mac, session.openid)
        if n <= 0:
            return u'绑定失败！没有该设备或者被占用。'
        session.nextState()
        print session.openid, session.state
        n = handle.userSave(session.openid, session.state)
        if n <= 0:
            return u'绑定失败！！'
        handle.close()
        return u'绑定成功！'
    else:
        handle.connect()
        if text == u'我的设备':
            rsp = str(handle.deviceQueryByUser(session.openid))
        elif text == u'解绑设备':
            session.nextState()
            handle.deviceUnbindByUser(session.openid)
            #handle.userSave(session.openid, session.state)
            handle.userDel(session.openid)
            rsp = u'解绑成功'
        elif text == u'开灯':
            han = handle.deviceQueryByUser(session.openid)
            if han[0][3] == 'OFF':
                rsp = u'设备离线'
            else:
                handle.deviceUpdateInfoByUser(session.openid, DbHandler.Info.format(12, 12, 'ON'))
                rsp = u'Waiting...'
        elif text == u'关灯':
            han = handle.deviceQueryByUser(session.openid)
            if han[0][3] == 'OFF':
                rsp = u'设备离线'
            else:
                handle.deviceUpdateInfoByUser(session.openid, DbHandler.Info.format(12, 12, 'OFF'))
                rsp = u'Waiting...'
        else:
            rsp = u'未知指令'
        handle.close()
        return rsp

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