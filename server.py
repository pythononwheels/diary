#
#
# diray server 
# khz / 2015
#

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import os.path
import sys

from controllers import *
from views.modules import *

from library.pow3_lib import APP_ID
from library.render_partial import RenderPatialModule

ui_modules = {
    'render_partial'     :   RenderPatialModule
}

app_settings = {
    "port"              :   443,
    "debug"             :   True,
    "template_path"     :   "./views",
    "ui_modules"        :   ui_modules,
    "static_path"       :   "./static",
    "static_url_prefix" :   "/static/",
    "cookie_secret"     :   APP_ID,
    "login_url"         :   "/login",
    "cookie_secret"     :   "254f2254-6bb0-1312-1104-3a0786ce285e"
    
}
server_settings =dict(
      ssl_options = {
        "certfile": os.path.join("certs/server.crt"),
        "keyfile": os.path.join("certs/server.key"),
        }
    )

routes = [
        (r'/login',                            LoginHandler),
        (r'/logout',                           LogoutHandler),
        (r'/goodbye',                          GoodByeHandler),
        (r'/diary/[^/]+',                          DiaryHandler),
        (r'/user/([^/]+)',                     UserHandler),
        (r'.*',                                LoginHandler)
        ]

if __name__ == "__main__":
 
    #tornado.options.parse_command_line()
    from tornado.log import enable_pretty_logging
    enable_pretty_logging()
    
    app = tornado.web.Application(handlers=routes, **app_settings)
    
    print("starting the diary Server ")
    print("visit: https://localhost:" + str(app_settings["port"]))
    print()
    #http_server = tornado.httpserver.HTTPServer(app)
    http_server = tornado.httpserver.HTTPServer(app, **server_settings)
    http_server.listen(app_settings["port"])

    tornado.ioloop.IOLoop.instance().start()