# -*- coding:utf8 -*-
import requests
import json

class QrcodeHandler:
    '''
    使用第三方的api实现二维码的识别与生成，http://pro.wwei.cn/open/api.html
    '''
    @staticmethod
    def parse(picurl):
        '''
        请求地址：http://api.wwei.cn/dewwei.html

        提交方式：POST、GET

        参数说明：

        名称	说明
        data	(必须) 二维码图片网络地址，开发者可以上传到自己服务器再提交地址过来
        apikey	(必须) 会员中心获取的apikey
        version	默认(1.0)
        请求示例：
        http://api.wwei.cn/dewwei.html?data=http://www.wwei.cn/Uploads/qrcode/2014/10/22/5447b8ba1c877.png&apikey=20141110217674

        返回示例：

        {
            "status":1,
            "msg":"success",
            "data":{
                "raw_data":"类型：URI<br/>内容：<a href="http://wwei.cn/" target="_blank">http://wwei.cn/</a>",
                "raw_text"=>"http://wwei.cn/",
                "raw_type":{
                    "key":"类型",
                    "value":"URI"
                },
                "raw_format":{
                    "key":"条形码格式",
                    "value":"QR_CODE"
                }
            }
        }
        返回说明：

        名称	说明
        status	0错误 1正常
        msg	错误时返回中文提示，成功时返回 success
        data
        raw_data	html 格式，可直接使用
        raw_type	类型
        URI	网址或链接
        TEXT	文本内容
        SMS	短信
        WIFI	wifi无线网络
        ADDRESSBOOK	名片
        TEL	电话号码
        EMAIL_ADDRESS	邮箱地址
        raw_format	条形码格式：QR_CODE 二维码

        :return:
        '''
        #picurl = u'http://blog.itpub.net/image/IT168.jpg'
        #20160309201826 是我的key
        '''parseUrl = u'http://api.wwei.cn/dewwei.html?data={0}&apikey=20160309201826'
        rsp = requests.get(parseUrl.format(picurl))
        print rsp.text
        result = json.loads(rsp.text)
        if result['status'] != 1:
            return None
        return result['data']['raw_text']'''
        parseUrl = 'http://www.2and1.cn/qrcode.do?cn=0&icode={0}'
        rsp = requests.get(parseUrl.format(picurl))
        print 'GET result QR:'+rsp.text
        return rsp.text

    @staticmethod
    def gen(reqData):
        '''
        请求地址：http://api.wwei.cn/wwei.html

        提交方式：POST、GET

        参数说明：

        名称	说明
        data	(必须) 二维码内容 ，请参考 二维码格式 说明
        apikey	(必须) 会员中心获取的apikey
        callback	(注意) 这是JSONP的callback参数，不为空会返回 JSONP 格式，查看示例
        level	纠错级别 默认L [ 'L','M','Q','H' ]，请参考 二维码格式 说明
        pse	生成格式 默认png [ 'png','svg','eps' ]
        bcolor	背景色 默认FFFFFF 白色，不用 # 号，下同
        fcolor	前景色 默认000000 黑色
        -------下面的只支持部分--------
        logo	[ jpg png gif ] 的logo http://eiv.baidu.com/hmt/icon/21.gif
        生成格式pse：只支持 png ，后期才支持 svg eps
        icolor	码眼的颜色 默认000000 黑色 只支持 png ，后期才支持 svg eps
        pcolor	码眼的边框颜色 默认000000 黑色 只支持 png ，后期才支持 svg eps
        xt	形态 默认1 [ 0液态 1直角 2圆圈 ] 只支持 png
        dwz	针对内容为url有效，默认0 [ 0不转换 1转换] 百度短网址 http://dwz.cn/
        zm	针对内容为url有效，默认0 [ 0不转换 1转换] 百度优化阅读 http://gate.baidu.com/
        version	默认1.0
        请求示例：http://api.wwei.cn/wwei.html?data=http%3A%2F%2Fwww.wwei.cn%2F&version=1.0&apikey=20141110217674

        返回示例：

        {
            "status":1,
            "msg":"success",
            "data":{
                "qr_filepath":"http://api.wwei.cn/Uploads/apiqrcode/2014/11/10/f03f5717616221de41881be555473a020.png",
                "qr_data":"http://www.baidu.com/",
                "new_descr":"",
                "new_version":0
                }
        }
        返回说明：

        名称	说明
        status	0错误 1正常
        msg	错误时返回中文提示，成功时返回 success
        data
        qr_filepath	二维码图片地址
        qr_data	二维码内容
        new_descr	(可忽略) 新版本提示（按您传的version判断）
        new_version	(可忽略) 0表示没新版，不等于0表示有新版本可以使用

        :return: qrcode的下载链接
        '''
        genUrl = u'http://api.wwei.cn/wwei.html?data={0}&version=1.0&apikey=20160309201826'
        rsp = requests.get(genUrl.format(reqData))
        result = json.loads(rsp.text)
        if result['status'] != 1:
            return None
        return result['data']['qr_filepath']

    @staticmethod
    def getImg(picUrl):
        '''
        请求地址：http://pro.wwei.cn/tmpdown.html

        提交方式：POST、GET

        参数：text 二维码图片网络地址

        示例：
        http://api.wwei.cn/Uploads/apiqrcode/2014/11/10/5ae42cee1b634de0951592822004ccb70.png
        :param picUrl:
        :return: 返回字节形式存储的响应。
        '''
        rsp = requests.get(picUrl, stream=True)
        return rsp.content

if __name__ == '__main__':
    url = QrcodeHandler.gen("test you haha")
    print url
    img = QrcodeHandler.getImg(url)
    f = open("test.jpg", 'wb')
    try:
        f.write(img)
    except Exception, e:
        print e.message
    f.close()