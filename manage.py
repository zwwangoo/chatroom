# -*- coding: utf-8 -*-
import torndb
import tornado.ioloop
import os
basePath = os.path.dirname(os.path.dirname(__file__))
from urls import application


if __name__ == "__main__":
    application.listen(8000, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
