# -*- coding:utf8 -*-
from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#应用程序启动
if __name__ == '__main__':
    wechat = WechatBasic(appid='wxbc6e508bcdd18484', appsecret='4a769c618b870a86e002dd0b1c15deb6')
    result = wechat.create_menu({
        'button':[
            {
                'type': 'click',
                'name': u'绑定设备',
                'key': 'V1001_TODAY_MUSIC'
            },
            {
                'type': 'click',
                'name': u'开/关',
                'key': 'V1001_TODAY_SINGER'
            }
        ]})
    print result