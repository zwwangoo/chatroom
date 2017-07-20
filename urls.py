import tornado.web

from chat import ChatHandler
from longpolling import LongPollingHandler
from reload import MainHandler, LoginHandler, LogoutHandler
from room import RoomHandler
from settings import settings


application = tornado.web.Application([
    (r"^/login$", LoginHandler),
    (r"^/index$", MainHandler),
    (r"^/room$", RoomHandler),
    (r"^/chat$", ChatHandler),
    (r"^/logout$", LogoutHandler),
    (r"^/longpolling$", LongPollingHandler),
], **settings)