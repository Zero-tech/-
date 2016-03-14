# -*- coding:utf8 -*-

class Session:
    '''
    利用状态机的特性模拟一个简单的会话，同时常驻在内存中。
    '''
    session_states = ('UNBIND', 'BINDED')
    def __init__(self, openid):
        self.openid = openid
        self.state = Session.session_states[0]
    def nextState(self):
        if self.state == Session.session_states[0]:
            self.state = Session.session_states[1]
        elif self.state == Session.session_states[1]:
            self.state = Session.session_states[0]