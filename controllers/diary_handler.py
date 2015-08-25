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
        posts = [
            { "title" : "ein erster Titel", "text" : "hier kommt jetzt der Text"},
            { "title" : "ein zweiter Titel", "text" : "hier kommt jetzt der Text"},
            { "title" : "ein dritter Titel", "text" : "hier kommt jetzt der Text"}
        ]
        #self.render("diary_cards_2.tmpl", posts=posts)
        #self.render("diary_bs4_cardstest_2.tmpl", posts=posts)
        self.render("diary_bs4_cardstest.tmpl", posts=posts, login=self.get_secure_cookie("login"))

    def on_finish(self):
        """
            Called after the end of a request.
        """
        pass


