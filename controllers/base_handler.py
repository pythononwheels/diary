import tornado.web
from tornado.log import app_log
import tornado.escape
import pprint

import os
import json

from tinydb import TinyDB, where

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("login")

    def print_debug_info(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        path = self.request.uri.split('?')[0]
        method = path.split('/')[-1]
        self.write("<hr>")
        self.write(str(self.__class__.__name__)+"<br>")
        self.write("path:" + path)
        self.write("<br>")
        self.write("method: " + method)
        self.write("<hr>")
        self.flush()

