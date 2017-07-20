#coding:utf-8
import time
import sys
import tornado.web
import tornadoredis
from tornado.escape import json_encode

class LongPollingHandler(tornado.web.RequestHandler):
    """"""
    @tornado.web.asynchronous
    def post(self):
        self.get_data()

    #连接到Redis 
    def initialize(self):
        self.client = tornadoredis.Client()
        self.client.connect()

    def get_roomchannel(self):
        # roomchannel = self.get_secure_cookie("roomid")
        roomchannel = 1
        return str(roomchannel)

    #订阅Redis的消息
    @tornado.gen.engine
    def subscribe(self):
        yield tornado.gen.Task(self.client.subscribe, self.get_roomchannel())
        self.client.listen(self.on_message)

    def get_data(self):
        if self.request.connection.stream.closed():
            print('***** closed and maybe lost!!!!! *****')
            return
       
        try:
            self.subscribe()
        except Exception, e :
            print(e,__file__,sys._getframe().f_lineon)
            pass

        #设置超时时间为60s
        num = 60
        self.time_handler = tornado.ioloop.IOLoop.instance().add_timeout(
            time.time()+num,
            lambda: self.on_timeout(num)
            )

    def on_timeout(self, num):
        self.time_handler = None
        self.send_data(json_encode({'name':'', 'msg':''}))
        if (self.client.connection.connected()):
            self.client.disconnect()

    #收到了Redis的消息
    def on_message(self, msg):
        if (msg.kind == 'message'):
            self.send_data(str(msg.body))
        elif (msg.kind == 'unsubscribe'):
            self.client.disconnect()

    #发送响应 
    def send_data(self, data):
        if self.request.connection.stream.closed():
            return

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        #print "set-data: ",data
        self.write(data)
        self.finish()