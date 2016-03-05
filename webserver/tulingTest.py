# -*- coding:utf8 -*-
import requests
import json
class Tl123Util:
    correct_code = {
        u'100000':u'文本',
        u'200000':u'链接',
        u'302000':u'新闻',
        u'308000':u'菜谱',
        u'313000':u'儿歌',
        u'314000':u'诗词'
    }
    correct_code_reverse = {
        u'文本':u'100000',
        u'链接':u'200000',
        u'新闻':u'302000',
        u'菜谱':u'308000',
        u'儿歌':u'313000',
        u'诗词':u'314000'
    }
    error_code = {
        u'40001':u'参数 key 错误',
        u'40002':u'请求内容 info 为空',
        u'40004':u'当天请求次数已使用完',
        u'40007':u'数据格式异常'
    }

class MsgTl123:
    def __init__(self, rspDic):
        try:
            self.code = str(rspDic['code'])
            self.text = rspDic['text']
            #print type(self.code), self.code, len(self.code)
            #print Tl123Util.error_code.keys()
            if self.code in Tl123Util.error_code.keys():
                self.tag = Tl123Util.error_code[self.code]
            self.tag = Tl123Util.correct_code[self.code]
        except Exception, e:
            print 'error ' + e.message
            self.code = '40000'
            self.text = 'Error'
            self.tag = 'Error'

class TextMsgtl123(MsgTl123):
    '''
    返回格式：
        {
            "code":100000,
            "text":"你也好 嘻嘻"
        }
    数据说明：
        字段      说明
        code    文本类标识码
        text      结果
    '''
    def __init__(self, rspDic):
        MsgTl123.__init__(self, rspDic)

class LinkMsgtl123(MsgTl123):
    '''
    返回格式：
        {
        "code": 200000,
        "text": "亲，已帮你找到图片",
        "url": "http://m.image.so.com/i?q=%E5%B0%8F%E7%8B%97"
        }
    数据说明:
        字段       说明
        code    链接类标识码
        text     提示语
        url      链接地址
    '''
    def __init__(self, rspDic):
        MsgTl123.__init__(self, rspDic)
        self.url = rspDic['url']

class Tl123:
    '''
    图灵123是封装了http://www.tuling123.com/的一个借口，用于向服务器发送数据，并解析结果。
        发送以post格式发送，接收会json的格式。且与图灵机器人交互是以文本形式进行的，返回的json数据有6种类型。
        发送数据体：
            key='appkey'&info='hi'&&userid='666'
        接收格式：
            {
                code:类型或者错误码         #必选
                text:回复正文或者提示语      #必选
                url:链接                   #可选
                list:列表等                #可选
                ...
                ...
            }
            Code 说明：
                正确码：
                    100000 文本类
                    200000 链接类
                    302000 新闻类
                    308000 菜谱类
                    313000（儿童版） 儿歌类
                    314000（儿童版） 诗词类
                异常码：
                    40001 参数 key 错误
                    40002 请求内容 info 为空
                    40004 当天请求次数已使用完
                    40007 数据格式异常
    '''

    #初始化函数，有默认key和默认url，如果网站更换可以显示传入
    def __init__(self, key = u'fb797154ee7dfe077a0c5734f7c5d0a8', url = 'http://www.tuling123.com/openapi/api'):
        #初始化私有变量，即post数据体
        self.__pData = dict()
        self.__pData['key'] = key
        self.__pData['info'] = u''
        self.__pData['userid'] = u''
        self.__url = url

    def requestMsg(self, info, userid = u'666'):
        self.__pData['info'] = info
        self.__pData['userid'] = userid
        rsp = requests.post(self.__url, self.__pData)
        rspDic = json.loads(rsp.text)
        if rspDic['code'] in Tl123Util.error_code.keys():
            #返回错误数据
            return MsgTl123(rspDic)
        if rspDic['code'] is Tl123Util.correct_code_reverse[u'文本']:
            return TextMsgtl123(rspDic)
        elif rspDic['code'] is Tl123Util.correct_code_reverse[u'链接']:
            return LinkMsgtl123(rspDic)
        else:
            return MsgTl123(rspDic)

if __name__ == '__main__':
    '''#simple test
    rData = {}
    rData['key'] = u'fb797154ee7dfe077a0c5734f7c5d0a8'
    rData['info'] = u'你好'
    rData['userid'] = u'666'
    rsp = requests.post('http://www.tuling123.com/openapi/api', rData)

    print rsp.text
    '''
    #test packed
    tl = Tl123()
    msg = tl.requestMsg(u'nicai~')
    print msg.code, msg.text, msg.tag