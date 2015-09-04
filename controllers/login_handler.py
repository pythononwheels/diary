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

    def signin_get(self):
        self.render("signin.tmpl")

    def signin_post(self):
        password = self.get_argument('password2', '')
        password2 = self.get_argument('password2', '')
        login = self.get_argument('login', '')
        
        if password != password2:
            self.render("error.tmpl", msg="Die Passwörter müssen übereinstimmen")
        
        u = User(login)
        if u.exists_in_db():
            self.render("error.tmpl", msg="Der Benutzer " + login 
                + " existiert bereits. Bitte melden sie sich einfach mit diesem Benuter an")
        else:
            # create user
            u.set_password(password)
            u.to_db()
            self.set_secure_cookie("login", login)
            print("set cookie: " + str(login))
            self.redirect("/diary/cards")

    def login_get(self):
        self.render("login.tmpl")

    def login_post(self):
        print("in login_post")
        password = self.get_argument('password', '')
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
            self.render("error.tmpl", msg="Der Benutzer " + login + " existiert nicht.")
  