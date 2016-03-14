__author__ = 'lg'
import requests
if __name__ ==  '__main__':
    #Insert
    '''reqData = dict()
    reqData['Op'] = 'Insert'
    reqData['MAC'] = '010201030406'
    rsp = requests.get('http://zerotech2016.applinzi.com/db', reqData)
    print rsp.text'''
    #Bind
    '''reqData = dict()
    reqData['Op'] = 'Bind'
    reqData['MAC'] = '010201030405'
    reqData['UserID'] = '20000'
    rsp = requests.get('http://zerotech2016.applinzi.com/db', reqData)
    print rsp.text'''
    #Unbind
    '''reqData = dict()
    reqData['Op'] = 'Unbind'
    reqData['MAC'] = '010201030405'
    reqData['UserID'] = '20000'
    rsp = requests.get('http://zerotech2016.applinzi.com/db', reqData)
    print rsp.text'''
    #UpdateInfo
    '''reqData = dict()
    reqData['Op'] = 'UpdateInfo'
    reqData['MAC'] = '010201030405'
    reqData['UserID'] = '10001'
    reqData['Info'] = '{Temp:21, Humi:35, Light:ON}'
    rsp = requests.get('http://zerotech2016.applinzi.com/db', reqData)
    print rsp.text'''
    #Off
    '''reqData = dict()
    reqData['Op'] = 'Off'
    reqData['MAC'] = '010201030405'
    rsp = requests.get('http://zerotech2016.applinzi.com/db', reqData)
    print rsp.text'''
    #Query
    reqData = dict()
    reqData['Op'] = 'Query'
    reqData['MAC'] = '010201030405'
    rsp = requests.get('http://zerotech2016.applinzi.com/db', reqData)
    print rsp.text
