# coding: utf-8
import json
import time
import tornado.web
from settings import db, redis_client


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user_id = self.get_secure_cookie("userid")
        if not user_id:return None
        return db.get("SELECT * FROM user WHERE id=%s", int(user_id))

    def exists_name_user(self, username):
        username = db.query("SELECT * FROM user WHERE username=%s", username)
        if len(username) > 0:return username[0]
        return None

class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html", title="登录")

    def post(self):
        user = self.exists_name_user(self.get_argument("name"))
        if user:
            if self.get_argument("password") == user.password:
                self.set_secure_cookie("userid", str(user.id))  # self.get_secure_cookie("user")
                redis_client.connect()
                redis_client.publish("userid", str(user.id))
                self.redirect("index")
            else:
                return self.write("<script>alert('密码错误!'); window.location.href='login';</script>")
        else:
            return self.write("<script>alert('用户不存在!'); window.location.href='login'</script>")


class RegisteredHandler(BaseHandler):

    def get(self):
        username = str(self.get_argument("username"))
        password = str(self.get_argument("password"))
        user = self.exists_name_user(username)
        if user:
            return self.write("<script>alert('用户名已存在！'); window.location.href='login'</script>")
        if username and password:
            try:
                db.execute("insert into user(username, password) values (%s, %s)", username, password)
            except:
                return self.redirect("login")
            return self.redirect("login")
        else:
            return self.write("<script>alert('必填项不能为空'); window.location.href='login'</script>")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_all_cookies()
        time.sleep(1)
        self.redirect("/login")


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        userid = self.get_current_user().id
        allRoom = db.query("SELECT room.id, roomname, created_time, username FROM room, user "
                           "WHERE room.owner_id=user.id")
        mineRoom = db.query("SELECT room.id, roomname, created_time, username FROM room, user "
                            "WHERE room.owner_id=%s AND user.id=%s", userid, userid)
        latelyRoom = db.query("SELECT room.id, roomname, created_time, user.username "
                            "FROM room, user WHERE user.id=room.owner_id "
                            "AND room.id IN (SELECT roomid FROM message WHERE message.userid=%s "
                            "GROUP BY roomid )", userid)
        self.render("index.html", allRoom=allRoom, mineRoom=mineRoom, latelyRoom=latelyRoom)


class ChatRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, roomId):
        userid = str(self.get_secure_cookie("userid"))
        if not db.query("SELECT * FROM room WHERE id=%s", roomId):
            return self.redirect("/index")
        self.set_secure_cookie("roomId", roomId)

        room = db.get("SELECT roomname FROM room WHERE id=%s", int(roomId))

        latelyRoom = db.query("SELECT room.id, roomname, created_time, user.username "
                              "FROM room, user WHERE user.id=room.owner_id "
                              "AND room.id IN (SELECT roomid FROM message WHERE message.userid=%s "
                              "GROUP BY roomid )", userid)

        owner_msg = db.query(
            "SELECT user.id, user.username, msg, created_time, type FROM message, user "
            "WHERE user.id=message.userid AND have_read=0 AND roomid=%s "
            "ORDER BY created_time;", roomId)

        room_msg = []
        userid_group = []
        user_group = []
        for msg_item in owner_msg:
            msg_group = {}
            if msg_item.type ==1:continue
            if msg_item.id not in userid_group:
                userid_group.append(msg_item.id)
                user_group.append({"username": msg_item.username, "userid": msg_item.id})
            msg_group["username"] = msg_item.username
            msg_group["created_time"] = msg_item.created_time.strftime('%Y-%m-%d %H:%M:%S')
            msg_group["msg"] = msg_item.msg
            msg_group["type"] = str(msg_item.type)
            if str(msg_item.id) == str(userid):
                msg_group["belong"] = 1
            else:
                msg_group["belong"] = 0
            room_msg.append(msg_group)
        self.render("chatroom.html", room=room, msg=room_msg, users=user_group, latelyRoom=latelyRoom)
