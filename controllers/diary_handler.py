from controllers.base_handler import BaseHandler

class DiaryHandler(BaseHandler):
    """
        general RequestHandler docu see : http://tornado.readthedocs.org/en/latest/web.html
    """
    
    def initialize(self):
        """
            A dictionary passed as the third argument of a url spec will 
            be supplied as keyword arguments to initialize().

            Example:
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
        """
        #self.database = database
        self.path = ""
        self.method = ""

    def cards_get(self):
        #self.print_debug_info()
        self.render("diary_cards.tmpl", login=self.get_secure_cookie("login"))

    def cards_get_mobile(self):
        #self.print_debug_info()
        self.render("diary_cards_mobile.tmpl", login=self.get_secure_cookie("login"))


    def new_get(self):
        self.write("new_get")
        self.flush()

    def on_finish(self):
        """
            Called after the end of a request.
        """
        pass


