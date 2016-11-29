#coding:utf-8
import os
import datetime
import torndb
import tornado.web
import json
import tornadoredis
from tornado.escape import json_encode

# # mysql 链接
db = torndb.Connection(
    host="127.0.0.1:3306", 
    database="chatroom",
    user="root",
    password="123456"
    )

c = tornadoredis.Client()
c.connect()

class ChatHandler(tornado.web.RequestHandler):
    """聊天"""

    @tornado.web.asynchronous
    def get(self):
        userid = str(self.get_secure_cookie("userid"))
        room_msg = []
        owner_msg = db.query("select userid, msg, created_time from message where have_read=0 and roomid order by created_time;")
        for msg_item in owner_msg:
            msg_group = {}
            msg_group["userid"] = msg_item.userid
            msg_group["createtime"] = msg_item.created_time.strftime('%Y-%m-%d %H:%M:%S')
            msg_group["msg"] = msg_item.msg
            if str(msg_item.userid) == str(userid):
                msg_group["belong"] = 1

            else:
                msg_group["belong"] = 0
            room_msg.append(msg_group)
        return self.write(json.dumps(room_msg))

    @tornado.web.asynchronous
    def post(self):
        roomchannel = 1
        userid = str(self.get_secure_cookie("userid"))
        message = str(self.get_argument("message"))
        data = json_encode({'name':userid, 'msg':message})
        
        createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("insert into message(userid, msg, roomid, created_time, have_read) values (%s, %s, 1, %s, 0)", 
            userid, message, createtime)
        #收到将消息publish到Redis
        #print data
        c.publish(roomchannel, data)
        
        self.write(json_encode({'result':True}))
        self.finish()

        
