import tornado.web
from tornado.log import app_log
import tornado.escape
import pprint

import os
import json

from tinydb import TinyDB, where

class BaseHandler(tornado.web.RequestHandler):

    #
    # Base Handler for the Controllers 
    #
    def get_current_user(self):
        return self.get_secure_cookie("login")

    def write_debug_info(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        #path = self.request.uri.split('?')[0]
        #method = path.split('/')[-1]
        
        self.write("Handler: " + str(self.__class__.__name__)+"<br>")
        self.write("<hr>")
        self.write(str(dir(self.request)))
        self.write("<br><hr>")
        self.write("query_arguments:" + str(self.request.query_arguments))
        self.write("<br>")
        self.write("uri:" + self.uri)
        self.write("<br>")
        self.write("path:" + self.path)
        self.write("<br>")
        self.write("method to call: " + self.request.method.lower() + "_" + self.method)
        self.write("<hr>")
        self.write("request method: " + self.request.method)
        self.write("<hr>")
        self.write("request headers: " + str(self.request.headers))
        self.write("<hr>")
        self.flush()

    def prepare(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        self.uri = self.request.uri
        self.path = self.request.uri.split('?')[0]
        self.method = self.path.split('/')[-1]
        self.default_methods = {}
        #
        # You can use the before_handler in a local controller to
        # process your own prepare stuff.
        # a common use case is to call: self.print_debug_info().
        # which then applies only to this specific handler.
        # 
        before_handler = getattr(self, "before_handler", None)
        print("calling before_handler for " +  str(self.__class__))
        if callable(before_handler):
            before_handler()
        

    def post(self):
        return self.dispatch(self.path, self.method)
    
    def get(self):
        return self.dispatch(self.path, self.method)

    def delete(self):
        return self.dispatch(self.path, self.method)

    def put(self):
        return self.dispatch(self.path, self.method)


    def dispatch(self, path, method):
        print("dispatch: http request method: " + self.request.method.lower())
        print("dispatch: uri: " +  self.uri)
        #print("dispatch: request dir: " +  str(dir(self.request)))
        print("dispatch: method: " +  self.method)
        print("dispatch: looking for action: " +  method + "_" + self.request.method.lower())
        action = getattr(self, method + "_" + self.request.method.lower(), None)
        if action:
            if callable(action):
                print("dispatch: action is: " + str(action))
                return action()
            else:
                raise tornado.web.HTTPError(404)
        elif self.request.method.lower() in self.default_methods:
            # check if there is a default action for this http request type and call that
            # this gives: get_login() if self.default_methods["get"] = "login"
            action = getattr(self, self.default_methods[self.request.method.lower()] + "_" + self.request.method.lower())
            return action()
        else:
            raise tornado.web.HTTPError(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('errors/404.tmpl',page=self.path)
        else:
            self.render('errors/unknown.tmpl',page=self.path)

