from controllers.base_handler import BaseHandler

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

    def get(self):
        self.render("login.html")

    def post(self):
        passwort = self.get_argument('passwort', '')
        swbkuerzel = self.get_argument('login', '')
        
        u = User(login)
        if u.exists_in_db():
            # user exists
            u.create_from_db()
            if u.check_password(passwort):
                # login ok
                self.set_secure_cookie("login", login)
                #self.render("mavs_manager.html", users=users_table.all())
                self.redirect("/diary/cards")
            else:
                # wrong passwort
                self.render("error.html", msg="Falsches Passwort für Benutzer: " + login )
        else:
            # user not in db
            self.render("error.html", msg="Der Benutzer " + login + " existiert nicht.")


    def prepare(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        pass

    def on_finish(self):
        """
            Called after the end of a request.
        """
        self.print_debug_info()
        