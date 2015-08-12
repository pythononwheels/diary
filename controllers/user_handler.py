from controllers.base_handler import *
from models.user import User

class UserHandler(BaseHandler):
    
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
    
    @tornado.web.authenticated
    def get(self, param):
        """ => user.list """
        swbkuerzel = self.get_current_user()
        #self.write("get (param): " + str(param))
        user = User(swbkuerzel)
        self.render("user_list.html", users=user.find_all())
        self.flush()

    def post(self):
        """  for now return a list of user plots"""
        pass

    def on_finish(self):
        """
            Called after the end of a request.
        """
        self.print_debug_info()
