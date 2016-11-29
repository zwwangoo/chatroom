# -*- coding: utf-8 -*-
import torndb
import tornado.ioloop
import tornado.web
import os
import datetime
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
basePath = os.path.dirname(os.path.dirname(__file__))

from login import LoginHandler, LogoutHandler
from room import RoomHandler, CreateRoomHandler, DropRoomHandler
from chat import ChatHandler
from longpolling import LongPollingHandler

# # mysql 链接
db = torndb.Connection(
    host="127.0.0.1:3306", 
    database="chatroom",
    user="root",
    password="123456"
    )
"""

execute                 执行语句不需要返回值的操作。
execute_lastrowid       执行后获得表id，一般用于插入后获取返回值。
executemany             可以执行批量插入。返回值为第一次请求的表id。
executemany_rowcount     批量执行。返回值为第一次请求的表id。
get                     执行后获取一行数据，返回dict。
iter                    执行查询后，返回迭代的字段和数据。
query                   执行后获取多行数据，返回是List。

"""

class MainHandler(tornado.web.RequestHandler):
    
    def get(self):
        userid = self.get_secure_cookie("userid")
        self.render("index.html", user=userid)


        
     
settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "template_path":os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "login_url": "/login",
    "xsrf_cookies":True,
    "debug":True,
}


application = tornado.web.Application([
    (r"^/login$", LoginHandler), 
    (r"^/index$", MainHandler), 
    (r"^/room$", RoomHandler),
    (r"^/chat$", ChatHandler),
    (r"^/logout$", LogoutHandler),
    (r"^/longpolling$", LongPollingHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8888, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
