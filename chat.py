#coding:utf-8
import os
import datetime
import tornado.web
import json
import tornadoredis
from tornado.escape import json_encode
from settings import db, redis_client
from reload import BaseHandler


class SendMsgHandler(tornado.web.RequestHandler):
    """聊天"""

    # @tornado.web.authenticated
    def post(self):
        roomchannel = self.get_secure_cookie("roomId")
        userid = str(self.get_secure_cookie("userid"))
        user = db.get("SELECT username FROM user WHERE id=%s", int(userid))
        message = str(self.get_argument("message"))
        msg_type = int(self.get_argument("type"))
        createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = json_encode({
            'username':user.username, 'msg':message,
            "userId":userid, "bglong": 0, "type": msg_type,
            "created_time": createtime
        })

        db.execute("insert into message(userid, msg, roomid, created_time, type) values (%s, %s, %s, %s, %s)",
            userid, message, roomchannel, createtime, msg_type)
        #收到将消息publish到Redis
        #print data
        redis_client.connect()
        redis_client.publish(roomchannel, data)
        self.write(json_encode({'result':True}))
        self.finish()


class CreateRoom(BaseHandler):

    def post(self):
        roomname = self.get_argument("roomname")
        password = self.get_argument("password")
        if roomname:
            room = db.query("SELECT * FROM room WHERE roomname=%s", roomname)
            if room:return self.write(json_encode({'result':2}))
        # try:
        createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        roomId = db.execute("INSERT INTO room (roomname, created_time, owner_id) VALUES (%s, %s, %s)",
                   roomname, createtime, self.get_secure_cookie("userid"))
        print roomId
        room = db.get("SELECT room.id, roomname, created_time, username FROM room, user WHERE room.id=%s and room.owner_id=user.id",
                        int(roomId))
        roomInfo = {}
        roomInfo["roomId"] = room.id
        roomInfo["roomname"] = room.roomname
        roomInfo["created_time"] = room.created_time.strftime('%Y-%m-%d %H:%M:%S')
        roomInfo["username"] = room.username
        return self.write(roomInfo)
        # except Exception as err:
        #     return self.set_status(500)







        
