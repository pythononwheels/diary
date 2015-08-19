from controllers.base_handler import BaseHandler
from models.user import User

class LoginHandler(BaseHandler):
    
    #
    # general RequestHandler docu see : http://tornado.readthedocs.org/en/latest/web.html
    #
    def initialize(self):
        """
            A dictionary passed as the third argument of a url spec will 
            be supplied as keyword arguments to initialize().

            Example:
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
        """
        #self.database = database
    def before_handler(self):
        self.default_methods["get"] = "login"
        self.default_methods["post"] = "login"


    def login_get(self):
        self.render("login.tmpl")

    def login_post(self):
        print("in login_post")
        passwort = self.get_argument('passwort', '')
        login = self.get_argument('login', '')
        
        u = User(login)
        if u.exists_in_db():
            # user exists
            u.create_from_db()
            self.set_secure_cookie("login", login)
            print("set cookie: " + str(login))
            self.redirect("/diary/cards")
        else:
            # user not in db
            self.render("error.html", msg="Der Benutzer " + login + " existiert nicht.")
  