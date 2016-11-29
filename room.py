#coding:utf-8
import os
import time
import torndb
import tornado.web

# # mysql 链接
db = torndb.Connection(
    host="127.0.0.1:3306", 
    database="chatroom",
    user="root",
    password="123456"
    )

class RoomHandler(tornado.web.RequestHandler):
    """ 获取所有在线房间 """
    def get(self):
        userid = self.get_secure_cookie("userid")
        msg = db.query("select userid, msg from message limit 20")
        self.render("room.html", msg=msg)


class CreateRoomHandler(tornado.web.RequestHandler):
	"""创建房间"""
	def __init__(self, arg):
		super(CreateRoomHandler, self).__init__()
		self.arg = arg
		

class DropRoomHandler(tornado.web.RequestHandler):
	"""删除房间"""
	def __init__(self, arg):
		super(DropRoomHandler, self).__init__()
		self.arg = arg
		