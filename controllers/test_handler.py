from controllers.base_handler import BaseHandler
from models.post import Post
import os
import tornado.web


class TestHandler(BaseHandler):
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
        print(str(self.__class__.__name__) + " initialize called!")
        self.path = ""
        self.method = ""
        

    def new_get(self, param=None):
        """ render the create new post form """
        #self.print_debug_info()
        
        print("Test Parameter: " + str(self.param_list))
        self.render("test_new.tmpl", login=self.get_current_user())

    def new_post(self):
        """ create the new post in table """
        self.write("test/new (POST)")
        

    def before_handler(self):
        self.default_methods["get"] = "new"
        self.default_methods["post"] = "new"

    def on_finish(self):
        """
            Called after the end of a request.
        """
        pass


