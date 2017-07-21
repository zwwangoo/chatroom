import tornado.web

from chat import SendMsgHandler
from longpolling import LongPollingHandler
from reload import MainHandler, LoginHandler, LogoutHandler, ChatRoomHandler, RegisteredHandler
from settings import settings


application = tornado.web.Application([
    (r"^/login$", LoginHandler),
    (r"^/logout$", LogoutHandler),
    (r"^/registered$", RegisteredHandler),
    (r"^/longpolling$", LongPollingHandler),

    (r"^/index$", MainHandler),

    (r"^/chatroom/([0-9]+)", ChatRoomHandler),
    (r"^/sendMsg$", SendMsgHandler),

], **settings)