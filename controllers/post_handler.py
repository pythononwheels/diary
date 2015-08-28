from controllers.base_handler import BaseHandler
from models.post import Post

IMAGE_UPLOAD_DIR = "../static/images/"

class PostHandler(BaseHandler):
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

    def new_get(self):
        """ render the create new post form """
        #self.print_debug_info()
        #self.render("post_new_form_test_bs_fileinput.tmpl", login=self.get_secure_cookie("login"))
        self.render("post_new_form_test_dropzone.tmpl", login=self.get_secure_cookie("login"))

    def new_post(self):
        """ create the new post in table """
        self.write("post/new (POST)")
        title = self.get_argument('post_title', '')
        text = self.get_argument('post_text', '')
        tags = self.get_argument("post_tags", None)
        is_event = self.get_argument("post_is_event", False)
        event = self.get_argument("post_event", None)

        photo = None
        photo = self.request.files['post_photo'][0]
        if photo:
            original_fname = photo['filename']
            extension = os.path.splitext(original_fname)[1]
            final_filename= IMAGE_UPLOAD_DIR+ original_fname+extension
            output_file = open(final_filename, 'wb')
            output_file.write(photo['body'])

        p = Post()
        p.title = title
        p.text = text
        if tags:
            p.tags = tags
        if is_event:
            p.event_text = event
        if photo:
            p.photo = final_filename

    def on_finish(self):
        """
            Called after the end of a request.
        """
        pass


