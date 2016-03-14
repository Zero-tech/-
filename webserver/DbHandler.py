# -*- coding:utf8 -*-
__author__ = 'yingjie'
import sae
import MySQLdb
'''sae.const.MYSQL_DB      # 数据库名
sae.const.MYSQL_USER    # 用户名
sae.const.MYSQL_PASS    # 密码
sae.const.MYSQL_HOST    # 主库域名（可读写）
sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
sae.const.MYSQL_HOST_S  # 从库域名（只读）
'''
class DbHandler:
    '''
    服务器字段说明：
        MAC   #设备MAC地址，为主键，不能重复，唯一
        USerID  #用户ID号 同时10001是系统用户，默认绑定在device上，但是不起作用
        Status  #状态，非激活(UNACTIVE 设备初始状态)
                      未绑定 (UNBIND 设备联网同步状态，但是没有用户绑定)
                      已绑定(BINDED 用户主动绑定设备)
        Online  #在线状态 在线 (ON 设备定时轮询向服务器同步状态，来保证在线状态，超时即为离线状态)
                         离线 (OFF 设备超时，即为离线)
        Info    #信息  (为设备同步的附加信息，向服务器同步当前的附加信息，格式为http的常用参数格式 eg Temp=21,Humi=35,Light=OFF
    '''
    Info = 'Temp={0},Humi={1},Light={2}'
    def __init__(self):
        self.__connect = None
        self.__cursor = None

    def connect(self):
        self.__connect = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                                 port=int(sae.const.MYSQL_PORT),
                                 user=sae.const.MYSQL_USER,
                                 passwd=sae.const.MYSQL_PASS,
                                 db=sae.const.MYSQL_DB,
                                 charset='utf8')
        self.__cursor = self.__connect.cursor()

    def insert(self, MAC, UserID=10001, Status='UNACTIVE', Online='OFF', Info='None'):
        query = 'insert into Device(MAC, UserID, Status, Online, Info) values (%s, %s, %s, %s, %s)'
        return self.__cursor.execute(query, (MAC, UserID, Status, Online, Info))

    def deviceBind(self, MAC, UserID, Status='BINDED'):
        query = 'update Device set UserID=%s, Status=%s where MAC=%s'
        n = self.__cursor.execute(query, (UserID, Status, MAC))
        self.__connect.commit()
        return n


    def deviceUnbind(self, MAC, UserID, Status='UNBIND'):
        query = 'update Device set UserID=%s, Status=%s where MAC=%s and UserID=%s'
        n = self.__cursor.execute(query, (10001, Status, MAC, UserID))
        self.__connect.commit()
        return n

    def deviceUnbindByUser(self, UserID, Status='UNBIND'):
        query = 'update Device set UserID=%s, Status=%s where UserID=%s'
        n = self.__cursor.execute(query, (10001, Status, UserID))
        self.__connect.commit()
        return n

    def deviceUpdateInfo(self, MAC, UserID, Info, Online='ON'):
        query = 'update Device set Info=%s, Online=%s where MAC=%s and UserID=%s'
        n = self.__cursor.execute(query, (Info, Online, MAC, UserID))
        self.__connect.commit()
        return n

    def deviceUpdateInfoByUser(self, UserID, Info, Online='ON'):
        query = 'update Device set Info=%s, Online=%s where UserID=%s'
        n = self.__cursor.execute(query, (Info, Online, UserID))
        self.__connect.commit()
        return n

    def deviceOff(self, MAC):
        query = 'update Device set Online=%s where MAC=%s'
        n = self.__cursor.execute(query, ('OFF', MAC))
        self.__connect.commit()
        return n

    def deviceQuery(self, MAC):
        query = 'select * from Device where MAC=%s'
        n = self.__cursor.execute(query, (MAC))
        return self.__cursor.fetchall()

    def deviceQueryByUser(self, userid):
        query = 'select * from Device where UserID=%s'
        n = self.__cursor.execute(query, (userid))
        if n <= 0:
            return None
        return self.__cursor.fetchall()

    def userInsert(self, openid, status):
        query = 'insert into Session(OpenID, Status) values (%s, %s)'
        n = self.__cursor.execute(query, (openid, status))
        if n <= 0:
            return None
        return self.__cursor.fetchall()
    def userQuery(self, openid):
        query = 'select * from Session where OpenID=%s'
        n = self.__cursor.execute(query, (openid))
        if n <= 0:
            return None
        return self.__cursor.fetchall()

    def userSave(self, openid, state):
        query = 'update Session set Status=%s where OpenID=%s'
        n = self.__cursor.execute(query, (state, openid))
        self.__connect.commit()
        return n

    def userDel(self, openid):
        query = 'delete from Session where OpenID=%s'
        n = self.__cursor.execute(query, (openid))
        self.__connect.commit()
        return n

    def close(self):
        self.__cursor.close()
        self.__connect.close()