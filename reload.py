# coding: utf-8
import time
import tornado.web
from settings import db


class MainHandler(tornado.web.RequestHandler):
    """主界面"""

    def get(self):
        userid = self.get_secure_cookie("userid")
        self.render("index.html", user=userid)


class LoginHandler(tornado.web.RequestHandler):
    """登录视图"""

    def get(self):
        self.render("login.html", title="登录")

    def post(self):  # get_argument() 方法来获取查询字符串参数，以及解析 POST 的内容
        user = db.query("select id, password from user where username=%s", self.get_argument("name"))
        if len(user) > 0:
            if self.get_argument("password") == user[0].password:
                self.set_secure_cookie("userid", str(user[0].id))  # self.get_secure_cookie("user")
                self.redirect("index")
            else:
                return self.write("<script>alert('密码错误!'); window.location.href='login';</script>")
        else:
            return self.write("<script>alert('用户不存在!'); window.location.href='login'</script>")


#注销
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        time.sleep(1)
        self.redirect("/login")


class RoomHandler(tornado.web.RequestHandler):
    """ 获取所有在线房间 """
    def get(self):
        userid = self.get_secure_cookie("userid")
        msg = db.query("select userid, msg from message order by created_time;")
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

