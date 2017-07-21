#coding:utf-8
import os
import datetime
import torndb
import tornado.web
import json
import tornadoredis
from tornado.escape import json_encode
from settings import db, redis_client


class SendMsgHandler(tornado.web.RequestHandler):
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
        user = db.get("SELECT username FROM user WHERE id=%s", int(userid))
        message = str(self.get_argument("message"))
        data = json_encode({'username':user.username, 'msg':message, "userId":userid, "bglong": 0})
        
        createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("insert into message(userid, msg, roomid, created_time, have_read) values (%s, %s, 1, %s, 0)", 
            userid, message, createtime)
        #收到将消息publish到Redis
        #print data
        redis_client.connect()
        redis_client.publish(roomchannel, data)
        self.write(json_encode({'result':True}))
        self.finish()


        
