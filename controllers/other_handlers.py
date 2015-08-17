from controllers.base_handler import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("login")
        self.redirect("/goodbye")

class GoodByeHandler(BaseHandler):
    def get(self):
        self.render("goodbye.tmpl")