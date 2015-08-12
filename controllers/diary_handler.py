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

    def get(self):
        self.write("get")
        self.flush()

    def post(self):
        """  for now return a list of user plots"""
        swbkuerzel = self.get_argument("swbkuerzel", None)
        plots=[]
        
        if swbkuerzel:
            allowed_plot_names = access_table.search(where("swbkuerzel") == swbkuerzel)
            for plot in allowed_plot_names:
                res = plots_table.search(where("plot_name") == plot["plot_name"] )
                if res:
                    plots.append(res[0])

        #self.write(",".join(plot_names))
        self.write(str(plots))
        self.flush()

    def prepare(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        self.path = self.request.uri.split('?')[0]
        self.method = self.path.split('/')[-1]
        

    def on_finish(self):
        """
            Called after the end of a request.
        """
        pass


